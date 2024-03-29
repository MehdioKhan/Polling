from django.db import models
from django.contrib.auth.models import User
from account.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
import uuid


class Translation(models.Model):
    language_code = models.CharField(max_length=25,blank=False,choices=settings.LANGUAGES)
    translation = models.CharField(max_length=250,blank=False)

    class Meta:
        abstract = True


class Poll(models.Model):
    name = models.CharField(max_length=150,blank=False,null=False)
    questions = models.ManyToManyField(to='Question')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name


class PollTranslation(Translation):
    poll = models.ForeignKey(to='Poll',on_delete=models.CASCADE,
                                related_name='translation')

    def __str__(self):
        return "{} translation in {}".format(self.poll.__str__(),self.language_code)


class Question(models.Model):
    body = models.CharField(max_length=150,blank=False,null=False)
    choices = models.ManyToManyField(to='Choice',related_name='question')
    position = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('position','created',)

    def __str__(self):
        return self.body

    def total_answers_count(self,user,poll):
        return self.answer.filter(to_user=user,poll_answer__poll=poll).count()

    def choices_answers_count(self,user,poll):
        result = {}
        for c in self.choices.all():
            result[c] = self.answer.filter(to_user=user,poll_answer__poll=poll,answer=c).count()
        return result

    def choices_percentage(self,user,poll):
        result = []
        total_answers = self.total_answers_count(user,poll)
        if total_answers:
            choice_answers_count = self.choices_answers_count(user,poll)
            for k,v in choice_answers_count.items():
                result.append((k,v/total_answers))
            return result
        else:
            raise ValueError('No one answered yet')

    def average(self,user,poll):
        sum = 0
        total = 0
        choices = self.choices.all().exclude(value=0)
        try:
            for c in choices:
                count = self.answer.filter(to_user=user, poll_answer__poll=poll, answer=c).count()
                sum += count*c.value
                total += count
            avg = sum / total * (100 / (self.choices.count()//2))
        except ZeroDivisionError:
            avg = 0
        return avg


class QuestionTranslation(Translation):
    question = models.ForeignKey(to='Question',on_delete=models.CASCADE,
                                    related_name='translation')

    def __str__(self):
        return "{} translation in {}".format(self.question.__str__(),self.language_code)


class Choice(models.Model):
    text = models.CharField(max_length=250,blank=True,null=False)
    value = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created','-value')

    def __str__(self):
        return '{0} - {1}'.format(self.text,str(self.value))


class ChoiceTranslation(Translation):
    choice = models.ForeignKey(to='Choice',on_delete=models.CASCADE,
                                  related_name='translation')

    def __str__(self):
        return "{} translation in {}".format(self.choice.__str__(),self.language_code)


class QuestionAnswer(models.Model):
    question = models.ForeignKey(to='Question',on_delete=models.CASCADE,
                                 related_name='answer')
    answer = models.ForeignKey(to='Choice',on_delete=models.CASCADE)
    to_user = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='question_answers')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('question',)

    def __str__(self):
        return "selected {} for {}".format(self.answer.text,self.question.body)

    def full_clean(self, exclude=None, validate_unique=True):
        valid_choices = self.question.choices.all()
        if self.answer not in valid_choices:
            raise ValidationError(
                'Selected choice "{}" is not one of the permitted values {}'.format(self.answer,valid_choices))
        super(QuestionAnswer,self).full_clean(exclude=exclude, validate_unique=validate_unique)


class PollAnswer(models.Model):
    poll = models.ForeignKey(to='Poll',on_delete=models.CASCADE)
    questions_answers = models.ManyToManyField(to='QuestionAnswer',related_name='poll_answer')
    to_user = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='answers')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return "answer to {} for {}".format(self.poll.name,self.to_user)


class RequestedPoll(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    poll = models.ForeignKey(to='Poll',on_delete=models.CASCADE,related_name='url')
    url_param = models.CharField(max_length=72,default=uuid.uuid4().hex,editable=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user','poll'),)
        ordering = ('-created',)

    def __str__(self):
        return self.url_param