from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new-post', views.new_post, name='new_post'),
    path('new-post/new-series', views.new_series, name='new_series'),
    path('logout', views.logout_view, name='logout'),
]
