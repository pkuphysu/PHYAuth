from django.urls import path

from . import views

app_name = 'cmsadmin'

urlpatterns = [
    path('announcement-list/', views.AnnouncementListView.as_view(), name='announcement-list'),
    path('announcement-create/', views.AnnouncementCreateView.as_view(), name='announcement-create'),
    path('announcement-update/', views.AnnouncementUpdateView.as_view(), name='announcement-update'),
    path('announcement-delete/', views.AnnouncementDeleteView.as_view(), name='announcement-delete'),

    path('toplink-list/', views.TopLinkListView.as_view(), name='toplink-list'),
    path('toplink-create/', views.TopLinkCreateView.as_view(), name='toplink-create'),
    path('toplink-update/', views.TopLinkUpdateView.as_view(), name='toplink-update'),
    path('toplink-delete/', views.TopLinkDeleteView.as_view(), name='toplink-delete'),

    path('oidc-client-faq-list/', views.OidcClientFaqListView.as_view(), name='oidc-client-faq-list'),
    path('oidc-client-faq-create/', views.OidcClientFaqCreateView.as_view(), name='oidc-client-faq-create'),
    path('oidc-client-faq-update/<int:pk>/', views.OidcClientFaqUpdateView.as_view(), name='oidc-client-faq-update'),
    path('oidc-client-faq-delete/', views.OidcClientFaqDeleteView.as_view(), name='oidc-client-faq-delete'),
]
