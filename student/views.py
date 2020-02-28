from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Subquery
from django.db.models import Q

from .models import *
from course.models import Course
from course.serializers import CourseSerializer
from question.models import Lesson
from question.serializers import LessonSerializer
from question.models import Question
from question.serializers import QuestionListSerializerStudent
from question.models import Answers
from question.models import LogQuestionUser


@csrf_exempt
@api_view(('GET',))
def courses(request):
    user = request.user

    courses_log = FinishedCourses.objects.filter(user=user.id)
    last_log = courses_log.last()

    if last_log is not None:
        course_objects = Course.objects.filter(id=Subquery(courses_log.values('course')))
        last_cours = Course.objects.get(pk=last_log.course.id)

        courses_data = CourseSerializer(course_objects, many=True).data
        next_courses_data = None

        if last_cours.next is not None:
            next_courses_data = CourseSerializer(last_cours.next).data

        response = {'taken': courses_data, 'next': next_courses_data}

        return Response(response, status=HTTP_200_OK, content_type="application/json")
    else:
        next = Course.objects.filter(prev=None).first()

        courses_data = CourseSerializer(next).data

        response = {'next': courses_data}

        return Response(response, status=HTTP_200_OK, content_type="application/json")


@csrf_exempt
@api_view(('GET',))
def lessons(request, course):
    user = request.user

    course_object = get_object_or_404(Course, pk=course)

    prev = course_object.prev

    if prev is not None:
        courses_log = FinishedCourses.objects.filter(user=user.id, course=prev.id).first()

        if courses_log is not None:
            lessons = Lesson.objects.filter(course=course_object.id)

            lessons_data = LessonSerializer(lessons, many=True).data

            return Response(lessons_data, status=HTTP_200_OK, content_type="application/json")
        else:
            return Response({'Error': 'Blocked Course'}, status=HTTP_200_OK, content_type="application/json")

    else:
        lessons = Lesson.objects.filter(course=course_object.id)

        lessons_data = LessonSerializer(lessons, many=True).data

        return Response(lessons_data, status=HTTP_200_OK, content_type="application/json")


@csrf_exempt
@api_view(('GET',))
def questions(request, lesson):
    user = request.user

    lesson_object = get_object_or_404(Lesson, pk=lesson)

    prev = lesson_object.prev

    if prev is not None:
        lessons_log = LogScoreUser.objects.filter(user=user.id, lesson=prev.id).first()

        if lessons_log is not None:
            questions = Question.objects.filter(lesson=lesson_object.id)

            question_data = QuestionListSerializerStudent(questions, many=True).data

            return Response(question_data, status=HTTP_200_OK, content_type="application/json")
        else:
            return Response({'Error': 'Blocked Lesson'}, status=HTTP_200_OK, content_type="application/json")

    else:
        questions = Question.objects.filter(lesson=lesson_object.id)

        question_data = QuestionListSerializerStudent(questions, many=True).data

        return Response(question_data, status=HTTP_200_OK, content_type="application/json")


@csrf_exempt
@api_view(('POST',))
def answer(request, lesson):
    user = request.user

    lesson_object = get_object_or_404(Lesson, pk=lesson)

    prev = lesson_object.prev

    def check_questions(response):
        count = 0
        print(response)
        for question in response:
            question_object = get_object_or_404(Question, pk=question['question'])
            answers = Answers.objects.filter(question=question_object, correct=True).values('id')

            if question_object.type == Question.A or question_object.type == Question.B or question_object.type == Question.D:
                correct = False
                array_to_compare = [item['id'] for item in answers]

                if array_to_compare == question['correct']:
                    count += question_object.score
                    correct = True

                loging = LogQuestionUser(user=user, question=question_object, lesson=lesson_object,
                                         correct=correct, points=question_object.score)
                loging.save()

            elif question_object.type == Question.C:
                correct = False

                for item in question['correct']:
                    if item in answers:
                        count += question_object.score
                        correct = True
                        break

                loging = LogQuestionUser(user=user, question=question_object, lesson=lesson_object,
                                         correct=correct, points=question_object.score)
                loging.save()
            else:
                return 0

        return count

    if prev is not None:
        lessons_log = LogScoreUser.objects.filter(user=user.id, lesson=prev.id).first()

        if lessons_log is not None:
            response = request.data.get("response")

            score = check_questions(response)

            log = LogScoreUser(user=user, lesson=lesson_object, points=score)
            log.save()

            if lesson_object.next is None:
                fin = FinishedCourses(user=user, course=lesson_object.course)
                fin.save()

            data = lesson_object.get_score(user)

            return Response(data, status=HTTP_200_OK, content_type="application/json")
        else:
            return Response({'Error': 'Blocked Lesson'}, status=HTTP_200_OK, content_type="application/json")

    else:
        response = request.data.get("response")

        score = check_questions(response)

        log = LogScoreUser(user=user, lesson=lesson_object, points=score)
        log.save()

        if lesson_object.next is None:
            fin = FinishedCourses(user=user, course=lesson_object.course)
            fin.save()

        data = lesson_object.get_score(user)

        return Response(data, status=HTTP_200_OK, content_type="application/json")





