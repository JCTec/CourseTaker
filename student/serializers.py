from rest_framework import serializers
from .models import *


class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogScoreUser
        depth = 1
        fields = '__all__'

