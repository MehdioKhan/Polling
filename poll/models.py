from django.db import models


class Poll(models.Model):
    name = models.CharField(max_length=150,blank=False,null=False)
    questions = models.ManyToManyField(to='Question',through='PollQuestion')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    body = models.CharField(max_length=150,blank=False,null=False)
    choices = models.ManyToManyField(to='Choice',through='QuestionChoice')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body


class Answer(models.Model):
    question = models.ForeignKey(to='Question',on_delete=models.CASCADE,
                                 related_name='answer')
    selected = models.ForeignKey(to='Choice',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.selected.text


class Choice(models.Model):
    text = models.CharField(max_length=250,blank=True,null=False)
    value = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} - {1}'.format(self.text,str(self.value))


class QuestionChoice(models.Model):
    question = models.ForeignKey(to='Question',on_delete=models.CASCADE)
    choice = models.ForeignKey(to='Choice',on_delete=models.CASCADE)

    def __str__(self):
        return '{0} - {1}'.format(self.question,self.choice)


class PollQuestion(models.Model):
    poll = models.ForeignKey(to='Poll',on_delete=models.CASCADE)
    question = models.ForeignKey(to='Question',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0} - {1}'.format(self.question,self.poll)