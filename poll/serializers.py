from rest_framework import serializers
from .models import Poll,Question,Choice


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ('pk','text','value')


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True,read_only=True)

    class Meta:
        model = Question
        fields = ('pk','body','choices')


class PollDetailsSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True,read_only=True)

    class Meta:
        model = Poll
        fields = ('id','name','questions')


class PollListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = ('pk','name')