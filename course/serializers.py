from rest_framework import serializers
from .models import *


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'pub_date')
