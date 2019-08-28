from django.urls import path
from . import views

app_name = 'polling'
question_answer_list = views.QuestionAnswerView.as_view({
    'get':'list',
    'post':'create',
})
question_answer_detail = views.QuestionAnswerView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
urlpatterns = [
    path('poll/list',views.PollList.as_view(),name='poll_list'),
    path('poll/<int:pk>',views.PollDetail.as_view(),name='poll_detail'),
    path('answer/<int:pk>',question_answer_detail,name='answer_detail'),
    path('answer/',question_answer_list,name='answer_list'),
]
