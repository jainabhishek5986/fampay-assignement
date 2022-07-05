from django.urls import path

from . import views

urlpatterns = [
    path('home', views.GetVideoDetails.as_view(), name='home_screen'),
    path('search_video', views.SearchVideo.as_view(), name='search_video'),
    path('add_keys', views.AddAPIKeys.as_view(), name='add_api_keys'),
]