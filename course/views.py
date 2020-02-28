from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .serializers import *
from .models import Course
from Middleware.ProfessorMiddleware import *


class CoursesAPI(APIView):

    @csrf_exempt
    @professor_middleware
    def get(self, request):
        courses = Course.objects.all()
        data = CourseSerializer(courses, many=True).data
        return Response(data, status=HTTP_200_OK, content_type="application/json")

    @csrf_exempt
    @professor_middleware
    def post(self, request):
        title = request.data.get("title")
        description = request.data.get("description")

        if title is None or description is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        course = Course(title=title, description=description, pub_date=timezone.now())
        course.save()

        data = CourseSerializer(course).data

        return Response(data, status=HTTP_200_OK)


class CourseAPI(APIView):
    @csrf_exempt
    @professor_middleware_id
    def get(self, request, id):

        course = get_object_or_404(Course, pk=id)

        if course is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        data = CourseSerializer(course).data

        return Response(data, status=HTTP_200_OK)

    @csrf_exempt
    @professor_middleware_id
    def put(self, request, id):

        course = get_object_or_404(Course, pk=id)

        if course is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        title = request.data.get("title")
        description = request.data.get("description")

        if title is None or description is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        course.title = title
        course.description = description

        course.save(update_fields=['title', 'description'])

        data = CourseSerializer(course).data

        return Response(data, status=HTTP_200_OK)

    @csrf_exempt
    @professor_middleware_id
    def delete(self, request, id):

        course = get_object_or_404(Course, pk=id)

        if course is None:
            return Response(status=HTTP_400_BAD_REQUEST)

        course.delete()

        data = {'status': 'Success'}

        return Response(data, status=HTTP_200_OK)

