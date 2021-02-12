from django.urls import path

from .views import *

app_name = 'pku_iaaa'

urlpatterns = [
    path('iaaa/', IAAALoginView.as_view(), name='iaaa_login'),
    path('iaaa/auth/', IAAALoginAuth.as_view(), name='iaaa_auth'),
]
