from django.urls import path

from live_tracker.views import refreshMain,start
from live_tracker import views
from .new_views import start
urlpatterns = [
    path("", views.HomePage, name="home"),
    path("api/refreshMain", refreshMain.as_view()),
    path("api/start", start.as_view()),
]
