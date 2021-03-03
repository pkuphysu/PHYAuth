from django.urls import path

from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.index, name='index'),
    path('contacts/', views.admins, name='admins'),

    path('announcement-list/', views.AnnouncementListView.as_view(), name='announcement-list'),
    path('announcement-create/', views.AnnouncementCreateView.as_view(), name='announcement-create'),
    path('announcement-update/<int:pk>/', views.AnnouncementUpdateView.as_view(), name='announcement-update'),
    path('announcement-delete/', views.AnnouncementDeleteView.as_view(), name='announcement-delete'),

    path('toplink-list/', views.TopLinkListView.as_view(), name='toplink-list'),
    path('toplink-create/', views.TopLinkCreateView.as_view(), name='toplink-create'),
    path('toplink-update/<int:pk>/', views.TopLinkUpdateView.as_view(), name='toplink-update'),
    path('toplink-delete/', views.TopLinkDeleteView.as_view(), name='toplink-delete'),
]
