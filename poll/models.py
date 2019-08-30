from django.db import models
from django.contrib.auth.models import User
from account.models import User
from django.core.exceptions import ValidationError


class Poll(models.Model):
    name = models.CharField(max_length=150,blank=False,null=False)
    questions = models.ManyToManyField(to='Question')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    body = models.CharField(max_length=150,blank=False,null=False)
    choices = models.ManyToManyField(to='Choice')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body


class Choice(models.Model):
    text = models.CharField(max_length=250,blank=True,null=False)
    value = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} - {1}'.format(self.text,str(self.value))


class QuestionAnswer(models.Model):
    question = models.ForeignKey(to='Question',on_delete=models.CASCADE,
                                 related_name='answer')
    selected = models.ForeignKey(to='Choice',on_delete=models.CASCADE)
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('question','user'),)

    def __str__(self):
        return "{} selected {} for {}".format(self.user,self.selected.text,self.question.body)

    def full_clean(self, exclude=None, validate_unique=True):
        valid_choices = self.question.choices.all()
        if self.selected not in valid_choices:
            raise ValidationError(
                'Selected choice "{}" is not one of the permitted values {}'.format(self.selected,valid_choices))
        super(QuestionAnswer,self).full_clean(exclude=exclude, validate_unique=validate_unique)


class PollAnswer(models.Model):
    poll = models.ForeignKey(to='Poll',on_delete=models.CASCADE)
    questions_answers = models.ManyToManyField(to='QuestionAnswer')
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} answered to {}".format(self.user,self.poll.name)