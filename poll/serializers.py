from rest_framework import serializers
from .models import Poll,Question,Choice,PollAnswer,QuestionAnswer,RequestedPoll
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
        fields = ('question','answer')

    def validate(self, attrs):
        valid_choices = attrs.get('question').choices.all()
        if attrs.get('answer') not in valid_choices:
            raise ValidationError(
                        'Selected choice "{}" is not one of the permitted values {}'.format(attrs.get('selected'), list(valid_choices)))
        return attrs


class PollAnswerSerializer(serializers.ModelSerializer):
    questions_answers = QuestionAnswerSerializer(many=True)

    class Meta:
        model = PollAnswer
        fields = ('poll','questions_answers','from_user','to_user')

    def create(self, validated_data):
        qas = validated_data['questions_answers']
        qaset = set()
        for item in qas:
            q = QuestionAnswer.objects.create(
                question=item['question'],
                answer=item['answer'],
                from_user=validated_data['from_user'],
                to_user=validated_data['to_user']
            )
            q.save()
            qaset.add(q)
        pa = PollAnswer.objects.create(
            poll=validated_data['poll'],
            from_user=validated_data['from_user'],
            to_user=validated_data['to_user'],
        )
        pa.questions_answers.set(qaset)

        pa.save()
        return pa


class RequestedPollCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestedPoll
        fields = ('user','poll')


class RequestedPollSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestedPoll
        fields = ('user','poll','url_param')


class QuestionAnswerDetailsSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = QuestionAnswer
        fields = ('question','answer')


class PollAnswerDetailsSerializer(serializers.ModelSerializer):
    questions_answers = QuestionAnswerDetailsSerializer(many=True,read_only=True)

    class Meta:
        model = PollAnswer
        fields = ('poll','questions_answers')


class ResultAnswerSerializer(serializers.Serializer):
    choice = serializers.CharField()
    percentage = serializers.FloatField()


class ResultSerializer(serializers.Serializer):
    question = serializers.CharField()
    answer = ResultAnswerSerializer(many=True)
