from django.urls import path

from live_tracker.views import UploadView, UploadPlay, refresh
from live_tracker import views

urlpatterns = [
    path("", views.HomePage, name="home"),
    path("playlist", views.Playlist, name="playlist"),
    path("api/upload-audio", UploadView.as_view()),
    path("api/upload-play", UploadPlay.as_view()),
    path("api/refresh", refresh.as_view()),
]
