from django.urls import path

#from live_tracker.views import refreshMain,start
#from live_tracker import views
from .new_views import start,youtube,segment,demo,source
urlpatterns = [
    #path("", views.HomePage, name="home"),
    #path("api/refreshMain", refreshMain.as_view()),
    path("api/start", start.as_view()),
    path("api/segment", segment.as_view()),
     path("api/demo", demo.as_view()),
     path("api/source", source.as_view()),
    path("api/youtube", youtube.as_view()),
]
