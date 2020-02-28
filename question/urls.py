from django.urls import include, path
from .views import *

urlpatterns = [
    path('course/<int:course>/lessons/', LessonAPI.as_view()),
    path('lesson/<int:id>/', LessonsAPI.as_view()),

    path('lesson/<int:lesson>/questions/', QuestionAPI.as_view()),
    path('question/<int:id>/', QuestionsAPI.as_view())
]
