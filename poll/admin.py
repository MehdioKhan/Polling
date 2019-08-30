from django.contrib import admin
from .models import Poll,Question,QuestionAnswer,Choice,PollAnswer,RequestedPoll


admin.site.register([Poll,Question,Choice,QuestionAnswer,PollAnswer,RequestedPoll])