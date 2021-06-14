from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('stats/', views.stats_page, name='stats'),
    path('events/', views.events_page, name='events'),
]