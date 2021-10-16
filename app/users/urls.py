from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('exit-clientgroup/', views.UserDelClientGroupView.as_view(), name='exit-clientgroup')
]
