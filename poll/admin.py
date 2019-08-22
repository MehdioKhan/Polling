from django.contrib import admin
from .models import Poll,Question,Answer,Choice,PollQuestion,QuestionChoice

admin.site.register([Poll,Question,PollQuestion,Answer,Choice,QuestionChoice])