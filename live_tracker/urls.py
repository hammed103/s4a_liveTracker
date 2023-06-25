from django.urls import path

from live_tracker.views import refreshMain
from live_tracker import views

urlpatterns = [
    path("", views.HomePage, name="home"),
    path("api/refreshMain", refreshMain.as_view()),
]
