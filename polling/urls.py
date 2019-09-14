from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polling/',include('poll.urls',namespace="polling")),
    path('accounts/',include('account.urls',namespace='accounts')),
]
