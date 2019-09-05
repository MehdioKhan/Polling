from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('signup',views.UserSignup.as_view(),name='signup'),
    path('user',views.logged_in_user_details)
]