from django.urls import path

from live_tracker.views import UploadView
from live_tracker import views


urlpatterns = [
    path("", views.HomePage, name="home"),
    path("api/upload-audio", UploadView.as_view()),
]
