from django.contrib import admin
from .models import Poll,Question,QuestionAnswer,Choice,\
    PollAnswer,RequestedPoll,ChoiceTranslation,QuestionTranslation,PollTranslation


admin.site.register([Poll,Question,Choice,QuestionAnswer,PollTranslation,
                     PollAnswer,RequestedPoll,ChoiceTranslation,QuestionTranslation])
