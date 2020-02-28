from rest_framework import serializers
from .models import *


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'description', 'course')


class AnswersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answers
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        depth = 1
        fields = '__all__'


class QuestionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        depth = 1
        fields = '__all__'

    def to_representation(self, obj):
        serializers = QuestionSerializer(obj)

        answers_object = Answers.objects.filter(question=obj)

        answers = AnswersSerializer(answers_object, many=True)

        response = serializers.data
        response['answers'] = answers.data

        return response


class AnswersSerializerStudent(serializers.ModelSerializer):

    class Meta:
        model = Answers
        fields = ('id', 'value')


class QuestionSerializerStudent(serializers.ModelSerializer):

    class Meta:
        model = Question
        depth = 1
        fields = ('id', 'value', 'score', 'lesson')


class QuestionListSerializerStudent(serializers.ModelSerializer):

    class Meta:
        model = Question
        depth = 1
        fields = '__all__'

    def to_representation(self, obj):
        serializers = QuestionSerializerStudent(obj)

        answers_object = Answers.objects.filter(question=obj)

        answers = AnswersSerializerStudent(answers_object, many=True)

        response = serializers.data
        response['answers'] = answers.data

        return response


