from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new-post', views.new_post, name='new_post'),
    path('new-post/new-series', views.new_series, name='new_series'),
    path('new-post/new-category', views.new_category, name='new_category'),
    path('new-post/cleanup', views.new_post_cleanup, name='cleanup'),
    path('post/<int:pk>/<slug:slug>', views.view_post, name='view_post'),
    path('logout', views.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

