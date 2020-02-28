from django.urls import include, path
from .views import *

urlpatterns = [
    path('', CoursesAPI.as_view()),
    path('<int:id>', CourseAPI.as_view())
]
