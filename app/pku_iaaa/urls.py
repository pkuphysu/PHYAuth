from django.urls import path

from .views import *

app_name = 'pku_iaaa'

urlpatterns = [
    path('login/', IAAALoginView.as_view(), name='iaaa_login'),
    path('auth/', IAAALoginAuth.as_view(), name='iaaa_auth'),
]
