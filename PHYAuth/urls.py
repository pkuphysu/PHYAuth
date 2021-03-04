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
    # login/
    # logout/
    # password_change/
    # password_reset/
    # reset/
    path('', include('django.contrib.auth.urls')),
    # authorize/
    # token/
    # userinfo/
    # end-session/
    # .well-known/openid-configuration/
    # introspect/
    # jwks/
    path('', include('oidc_provider.urls', namespace='oidc_provider')),
    # profile/
    # client-create/
    # client-update/
    # client-list/
    path('', include('app.users.urls', namespace='users')),
    # /
    path('', portal_views.index, name='index'),
    path('', include('app.portal.urls', namespace='portal')),
    # iaaa/login
    # iaaa/auth
    path('iaaa/', include('app.pku_iaaa.urls', namespace='pku_iaaa')),
    # admin/
    path(f'{settings.ADMIN_URL}', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))
    ]
