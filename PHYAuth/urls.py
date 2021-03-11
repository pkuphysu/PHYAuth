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

from app.portal import views as portal_views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    # accounts/login/
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
    path('oidc/', include('oidc_provider.urls', namespace='oidc_provider')),
    # iaaa/login
    # iaaa/auth
    path('iaaa/', include('app.pku_iaaa.urls', namespace='pku_iaaa')),
    # /
    # contacts/
    path('', portal_views.index, name='index'),
    path('', include('app.portal.urls', namespace='portal')),
    # announcement-*/
    # toplink-*/
    path('', include('app.cmsadmin.urls', namespace='cmsadmin')),
    # secret-admin-url/
    path(f'{settings.ADMIN_URL}', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]
