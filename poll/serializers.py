from rest_framework import serializers
from .models import Poll,Question,Choice,PollAnswer,QuestionAnswer
from rest_framework.exceptions import ValidationError


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


class QuestionAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionAnswer
        fields = ('question','selected')

    def validate(self, attrs):
        valid_choices = attrs.get('question').choices.all()
        if attrs.get('selected') not in valid_choices:
            raise ValidationError(
                        'Selected choice "{}" is not one of the permitted values {}'.format(attrs.get('selected'), list(valid_choices)))
        return attrs


class PollAnswerSerializer(serializers.ModelSerializer):
    questions_answers = QuestionAnswerSerializer(many=True)

    class Meta:
        model = PollAnswer
        fields = ('poll','questions_answers','user')

    def create(self, validated_data):
        qas = validated_data['questions_answers']
        qaset = set()
        for item in qas:
            q=QuestionAnswer.objects.create(
                question=item['question'],
                selected=item['selected'],
                user=validated_data['user']
            )
            q.save()
            qaset.add(q)
        pa = PollAnswer.objects.create(
            poll=validated_data['poll'],
            user=validated_data['user'],
        )
        pa.questions_answers.set(qaset)

        pa.save()
        return pa
