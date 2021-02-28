from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('client-create/', views.ClientCreateView.as_view(), name='client-create'),
    path('client-list/', views.ClientListView.as_view(), name='client-list'),
    path('client-update/<int:pk>/', views.ClientUpdateView.as_view(), name='client-update'),
]
