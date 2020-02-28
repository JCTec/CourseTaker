from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models import Max

from .serializers import *
from course.models import Course
from .models import *
from Middleware.ProfessorMiddleware import *


class LessonAPI(APIView):

    @csrf_exempt
    @professor_middleware_course
    def get(self, request, course):
        course_object = get_object_or_404(Course, pk=course)
        lessons = Lesson.objects.filter(course=course_object.id)
        data = LessonSerializer(lessons, many=True).data
        return Response(data, status=HTTP_200_OK, content_type="application/json")

    @csrf_exempt
    @professor_middleware_course
    def post(self, request, course):
        course_object = get_object_or_404(Course, pk=course)

        title = request.data.get("title")
        description = request.data.get("description")

        if title is None or description is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        lesson = Lesson(course=course_object, title=title, description=description)
        lesson.save()

        data = LessonSerializer(lesson).data

        return Response(data, status=HTTP_200_OK, content_type="application/json")


class LessonsAPI(APIView):
    @csrf_exempt
    @professor_middleware_id
    def get(self, request, id):

        lesson = get_object_or_404(Lesson, pk=id)

        if lesson is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        data = LessonSerializer(lesson).data

        return Response(data, status=HTTP_200_OK)

    @csrf_exempt
    @professor_middleware_id
    def put(self, request, id):
        lesson = get_object_or_404(Lesson, pk=id)

        if lesson is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        title = request.data.get("title")
        course = request.data.get("course")
        description = request.data.get("description")

        has_update = False

        if course is not None:
            course_object = get_object_or_404(Course, pk=course)
            lesson.course = course_object
            has_update = True

        if title is not None:
            lesson.title = title
            has_update = True

        if description is not None:
            lesson.description = description
            has_update = True

        if has_update:
            lesson.save(update_fields=['course', 'description'])
            data = LessonSerializer(lesson).data

            return Response(data, status=HTTP_200_OK)
        else:
            return Response({'status': 'No update was made'}, status=HTTP_200_OK)

    @csrf_exempt
    @professor_middleware_id
    def delete(self, request, id):
        lesson = get_object_or_404(Lesson, pk=id)

        if lesson is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        lesson.delete()

        data = {'status': 'Success'}

        return Response(data, status=HTTP_200_OK)


class QuestionAPI(APIView):

    @csrf_exempt
    @professor_middleware_lesson
    def get(self, request, lesson):
        lesson_object = get_object_or_404(Lesson, pk=lesson)
        questions = Question.objects.filter(lesson=lesson_object.id)
        data = QuestionListSerializer(questions, many=True).data
        return Response(data, status=HTTP_200_OK, content_type="application/json")

    @csrf_exempt
    @professor_middleware_lesson
    def post(self, request, lesson):
        lesson_object = get_object_or_404(Lesson, pk=lesson)

        type = request.data.get("type")
        value = request.data.get("value")
        score = request.data.get("score")
        answer = request.data.get("answer")

        question = Question(lesson=lesson_object, value=value, type=type, score=score)
        question.save()

        for item in answer:
            answer_object = Answers(question=question, value=item['value'], correct=item['correct'])
            answer_object.save()

        data = QuestionListSerializer(question).data

        return Response(data, status=HTTP_200_OK, content_type="application/json")


class QuestionsAPI(APIView):
    @csrf_exempt
    @professor_middleware_id
    def get(self, request, id):
        question = get_object_or_404(Question, pk=id)

        if question is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        data = QuestionListSerializer(question).data

        return Response(data, status=HTTP_200_OK)

    @csrf_exempt
    @professor_middleware_id
    def put(self, request, id):
        return Response({'Status': 'Route not implemented'}, status=HTTP_200_OK)


    @csrf_exempt
    @professor_middleware_id
    def delete(self, request, id):
        question = get_object_or_404(Question, pk=id)

        if question is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        question.delete()

        data = {'status': 'Success'}

        return Response(data, status=HTTP_200_OK)
