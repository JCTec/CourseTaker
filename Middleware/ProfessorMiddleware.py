from django.contrib.auth import authenticate
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED
)
from rest_framework.response import Response


def professor_middleware(get_response):

    def middleware(self, request):
        if request.user.is_professor:
            response = get_response(self, request)
            return response
        else:
            error = {'error': 'User not a professor'}
            return Response(error, status=HTTP_401_UNAUTHORIZED, content_type="application/json")

    return middleware


def professor_middleware_lesson(get_response):

    def middleware(self, request, lesson):
        if request.user.is_professor:
            response = get_response(self, request, lesson)
            return response
        else:
            error = {'error': 'User not a professor'}
            return Response(error, status=HTTP_401_UNAUTHORIZED, content_type="application/json")

    return middleware


def professor_middleware_course(get_response):

    def middleware(self, request, course):
        if request.user.is_professor:
            response = get_response(self, request, course)
            return response
        else:
            error = {'error': 'User not a professor'}
            return Response(error, status=HTTP_401_UNAUTHORIZED, content_type="application/json")

    return middleware


def professor_middleware_id(get_response):

    def middleware(self, request, id):
        if request.user.is_professor:
            response = get_response(self, request, id)
            return response
        else:
            error = {'error': 'User not a professor'}
            return Response(error, status=HTTP_401_UNAUTHORIZED, content_type="application/json")

    return middleware

