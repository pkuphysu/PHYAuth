from django.urls import path

from . import views

app_name = 'oidc_client'
urlpatterns = [
    path('faq/', views.FaqListView.as_view(), name='faq'),
    path('client-create/', views.ClientCreateView.as_view(), name='client-create'),
    path('client-list/', views.ClientListView.as_view(), name='client-list'),
    path('client-update/<int:pk>/', views.ClientUpdateView.as_view(), name='client-update'),

    path('clientgroup-list/', views.ClientGroupListView.as_view(), name='clientgroup-list'),
    path('clientgroup-create/', views.ClientGroupCreateView.as_view(), name='clientgroup-create'),
    path('clientgroup-update/<int:pk>/', views.ClientGroupUpdateView.as_view(), name='clientgroup-update'),
    path('clientgroup-delete/', views.ClientGroupDeleteView.as_view(), name='clientgroup-delete'),

    path('clientgroup/<int:gid>/user/', views.ClientGroupUsersListView.as_view(), name='clientgroup-user'),
    path('clientgroup/<int:gid>/invite/<str:signstr>/', views.ClientGroupInviteUserAcceptView.as_view(),
         name='clientgroup-user-invite-accept'),
    path('clientgroup/<int:gid>/invite/', views.ClientGroupInviteUserView.as_view(), name='clientgroup-user-invite'),
    path('clientgroup/<int:gid>/reinvite/', views.ClientGroupReinvteUserView.as_view(), name='clientgroup-user-reinvite'),
    path('clientgroup/<int:gid>/delete/', views.ClientGroupDelUserView.as_view(), name='clientgroup-user-delete'),
]
