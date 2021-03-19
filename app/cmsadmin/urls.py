from django.urls import path

from .views import oidc_client_view, portal_view, users_view

app_name = 'cmsadmin'

urlpatterns = []

# portal manage view
urlpatterns += [
    path('portal-announcement-list/', portal_view.AnnouncementListView.as_view(), name='portal-announcement-list'),
    path('protal-announcement-create/', portal_view.AnnouncementCreateView.as_view(),
         name='portal-announcement-create'),
    path('portal-announcement-update/', portal_view.AnnouncementUpdateView.as_view(),
         name='portal-announcement-update'),
    path('portal-announcement-delete/', portal_view.AnnouncementDeleteView.as_view(),
         name='portal-announcement-delete'),

    path('portal-toplink-list/', portal_view.TopLinkListView.as_view(), name='portal-toplink-list'),
    path('portal-toplink-create/', portal_view.TopLinkCreateView.as_view(), name='portal-toplink-create'),
    path('portal-toplink-update/', portal_view.TopLinkUpdateView.as_view(), name='portal-toplink-update'),
    path('portal-toplink-delete/', portal_view.TopLinkDeleteView.as_view(), name='portal-toplink-delete'),
]

# users manage view
urlpatterns += [
    path('users-user-list/', users_view.UserListView.as_view(), name='users-user-list'),
    path('users-user-create/', users_view.UserCreateView.as_view(), name='users-user-create'),
    path('users-user-update/', users_view.UserUpdateView.as_view(), name='users-user-update'),
    path('users-user-group-update/', users_view.UserGroupUpdateView.as_view(), name='users-user-group-update'),
    path('users-user-delete/', users_view.UserDeleteView.as_view(), name='users-user-delete'),

    path('users-departement-list/', users_view.DepartmentListView.as_view(), name='users-department-list'),
    path('users-departement-create/', users_view.DepartmentCreateView.as_view(), name='users-department-create'),
    path('users-departement-update/', users_view.DepartmentUpdateView.as_view(), name='users-department-update'),
    path('users-departement-delete/', users_view.DepartmentDeleteView.as_view(), name='users-department-delete'),
]

# oidc manage view
urlpatterns += [
    path('oidc-client-faq-list/', oidc_client_view.OidcClientFaqListView.as_view(), name='oidc-client-faq-list'),
    path('oidc-client-faq-create/', oidc_client_view.OidcClientFaqCreateView.as_view(), name='oidc-client-faq-create'),
    path('oidc-client-faq-update/', oidc_client_view.OidcClientFaqUpdateView.as_view(), name='oidc-client-faq-update'),
    path('oidc-client-faq-delete/', oidc_client_view.OidcClientFaqDeleteView.as_view(), name='oidc-client-faq-delete'),
]
