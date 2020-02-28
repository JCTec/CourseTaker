from django.db import models
from users.models import User
from question.models import Lesson
from course.models import Course


class LogScoreUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True)
    points = models.IntegerField()


class FinishedCourses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)

