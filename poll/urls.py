from django.urls import path
from . import views

app_name = 'polling'

urlpatterns = [
    path('poll/list',views.PollList.as_view(),name='poll_list'),
    path('poll/<int:pk>',views.PollDetail.as_view(),name='poll_detail'),
]
