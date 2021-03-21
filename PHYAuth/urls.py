"""PHYAuth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from oidc_provider import views as oidc_provider_views

from app.portal import views as portal_views
from app.users import views as users_views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    # accounts/login/
    path('accounts/login/', users_views.MyLoginView.as_view(), name='login'),
    # accounts/logout/
    # accounts/password_change/
    # accounts/password_reset/
    # accounts/reset/
    path('accounts/', include('django.contrib.auth.urls')),
    # accounts/profile/
    # accounts/client-create/
    # accounts/client-update/
    # accounts/client-list/
    path('accounts/', include('app.users.urls', namespace='users')),
    # oidc/authorize/
    # oidc/token/
    # oidc/userinfo/
    # oidc/end-session/
    # oidc/.well-known/openid-configuration/
    # oidc/introspect/
    # oidc/jwks/
    path('.well-known/openid-configuration/', oidc_provider_views.ProviderInfoView.as_view(), name='provider-info'),
    path('oidc/', include('oidc_provider.urls', namespace='oidc_provider')),
    # iaaa/login
    # iaaa/auth
    path('iaaa/', include('app.pku_iaaa.urls', namespace='pku_iaaa')),
    # /
    # contacts/
    path('', portal_views.index, name='index'),
    path('', include('app.portal.urls', namespace='portal')),
    # oidc-client/client-*/
    path('oidc-client/', include('app.oidc_client.urls', namespace='oidc_client')),
    # cmsadmin/announcement-*/
    # cmsadmin/toplink-*/
    path('cmsadmin/', include('app.cmsadmin.urls', namespace='cmsadmin')),
    # secret-admin-url/
    path(f'{settings.ADMIN_URL}', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]
