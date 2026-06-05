from django.urls import path
from . import views

urlpatterns = [
    # main pages
    path('', views.index, name='index'),
    path('videos/', views.video_listing, name='video_listing'),
    path('videos/add/', views.add_video, name='add_video'),
]