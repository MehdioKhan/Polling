from rest_framework import serializers
from .models import Poll,Question,Choice,PollAnswer,QuestionAnswer,RequestedPoll,\
    PollTranslation,QuestionTranslation,ChoiceTranslation
from rest_framework.exceptions import ValidationError


class ChoiceSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField('get_translated_text')

    class Meta:
        model = Choice
        fields = ('pk','text','value')

    def get_translated_text(self,instance):
        language = self.context.get('request').META.get('HTTP_ACCEPT_LANGUAGE')[:2].lower()
        pk = instance.pk
        text = Choice.objects.get(pk=pk).text
        try:
            text = ChoiceTranslation.objects.get(language_code=language,choice=pk).translation
        except:
            pass
        return text


class QuestionSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField('get_choice_serializer')
    body = serializers.SerializerMethodField('get_translated_body')

    class Meta:
        model = Question
        fields = ('pk','body','choices')

    def get_choice_serializer(self,instance):
        choices = Choice.objects.filter(question=instance.pk)
        serializer = ChoiceSerializer(choices,many=True,read_only=True,context=self.context)
        return serializer.data

    def get_translated_body(self,instance):
        language = self.context.get('request').META.get('HTTP_ACCEPT_LANGUAGE')[:2].lower()
        pk = instance.pk
        text = Question.objects.get(pk=pk).body
        try:
            text = QuestionTranslation.objects.get(language_code=language,question=pk).translation
        except:
            pass
        return text


class PollDetailsSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField('get_question_serializer')
    name = serializers.SerializerMethodField('get_translated_name')

    class Meta:
        model = Poll
        fields = ('id','name','questions')

    def get_question_serializer(self,instance):
        qs = Question.objects.filter(poll=instance.pk)
        serializer = QuestionSerializer(qs,many=True,read_only=True,context=self.context)
        return serializer.data

    def get_translated_name(self,instance):
        language = self.context.get('request').META.get('HTTP_ACCEPT_LANGUAGE')[:2].lower()
        pk = instance.pk
        text = Poll.objects.get(pk=pk).name
        try:
            text = PollTranslation.objects.get(language_code=language,poll=pk).translation
        except:
            pass
        return text


class PollListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField('get_translated_name')

    class Meta:
        model = Poll
        fields = ('pk','name')

    def get_translated_name(self,instance):
        language = self.context.get('request').META.get('HTTP_ACCEPT_LANGUAGE')[:2].lower()
        pk = instance.pk
        text = Poll.objects.get(pk=pk).name
        try:
            text = PollTranslation.objects.get(language_code=language,poll=pk).translation
        except:
            pass
        return text


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
        fields = ('poll','questions_answers','to_user')

    def create(self, validated_data):
        qas = validated_data['questions_answers']
        qaset = set()
        for item in qas:
            q = QuestionAnswer.objects.create(
                question=item['question'],
                answer=item['answer'],
                to_user=validated_data['to_user']
            )
            q.save()
            qaset.add(q)
        pa = PollAnswer.objects.create(
            poll=validated_data['poll'],
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
    question = serializers.SerializerMethodField('get_question_serializer')

    class Meta:
        model = QuestionAnswer
        fields = ('question','answer')

    def get_question_serializer(self,instance):
        qs = Question.objects.filter(poll=instance.pk)
        serializer = QuestionSerializer(qs,read_only=True,context=self.context)
        return serializer.data


class PollAnswerDetailsSerializer(serializers.ModelSerializer):
    questions_answers = serializers.SerializerMethodField('get_question_answer_serializer')

    class Meta:
        model = PollAnswer
        fields = ('poll','questions_answers')

    def get_question_answer_serializer(self,instance):
        qas = QuestionAnswer.objects.filter(poll_answer=instance.pk)
        serializer = QuestionAnswerDetailsSerializer(qas,many=True,read_only=True,context=self.context)
        return serializer.data


class ResultAnswerSerializer(serializers.Serializer):
    choice = serializers.SerializerMethodField('get_choice_serializer')
    percentage = serializers.FloatField()

    def get_choice_serializer(self,instance):
        c = Choice.objects.filter(question=instance.pk)
        serializer = ChoiceSerializer(c,context=self.context)
        return serializer.data
