from django.urls import path
from . import views

app_name = 'polling'

poll_answer_list = views.PollAnswerView.as_view({
    'get':'list',
    'post':'create',
})
poll_answer_detail = views.PollAnswerView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
urlpatterns = [
    path('poll/list',views.PollList.as_view(),name='poll_list'),
    path('poll/<int:pk>',views.PollDetail.as_view(),name='poll_detail'),
    path('quiz/<slug:param>',views.answer_poll_by_link),
    path('poll/answer',poll_answer_list),
    path('poll/link',views.poll_link_create),
    path('poll/result',views.get_poll_answers)
]
