from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile')
    # path('register/', views.register, name='register'),
]
