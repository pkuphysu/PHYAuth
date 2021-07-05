from django.urls import path

from . import views

app_name = 'oidc_client'
urlpatterns = [
    path('faq/', views.FaqListView.as_view(), name='faq'),
    path('client-create/', views.ClientCreateView.as_view(), name='client-create'),
    path('client-list/', views.ClientListView.as_view(), name='client-list'),
    path('client-update/<int:pk>/', views.ClientUpdateView.as_view(), name='client-update'),

    path('appgroup-list/', views.AppGroupListView.as_view(), name='appgroup-list'),
    path('appgroup-create/', views.AppGroupCreateView.as_view(), name='appgroup-create'),
    path('appgroup-update/<int:pk>/', views.AppGroupUpdateView.as_view(), name='appgroup-update'),
    path('appgroup-delete/', views.AppGroupDeleteView.as_view(), name='appgroup-delete'),

    path('appgroup/<int:gid>/user/', views.AppGroupUserListView.as_view(), name='appgroup-user'),
    path('appgroup/<int:gid>/invite/<str:signstr>/', views.AppGroupInviteUserAcceptView.as_view(),
         name='appgroup-user-invite-accept'),
    path('appgroup/<int:gid>/invite/', views.AppGroupInviteUserView.as_view(), name='appgroup-user-invite'),
    path('appgroup/<int:gid>/delete/', views.AppGroupDelUserView.as_view(), name='appgroup-user-delete'),
]
