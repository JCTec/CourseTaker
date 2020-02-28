from django.urls import include, path
from .views import *

urlpatterns = [
    path('course/', courses),
    path('lesson/<int:course>', lessons),
    path('question/<int:lesson>', questions),
    path('answer/<int:lesson>', answer)
]
