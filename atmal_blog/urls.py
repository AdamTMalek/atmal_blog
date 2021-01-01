"""atmal_blog URL Configuration"""
from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('atmalblog.urls')),
    re_path(r'^markdownx/', include('markdownx.urls')),
]
