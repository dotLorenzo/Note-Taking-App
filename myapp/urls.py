"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from oauth import views as oauth_views

urlpatterns = [
	path('', include('feed.urls')),
    path('admin/', admin.site.urls),

    path('oauth/', oauth_views.index, name="evernote_index"),
    path('oauth/auth/post/<int:post_id>/', oauth_views.auth, name="evernote_auth"),
    path("oauth/callback/", oauth_views.callback, name="evernote_callback"),
    path("oauth/reset/", oauth_views.reset, name="evernote_auth_reset")
]

handler404 = 'feed.views.error_404'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)