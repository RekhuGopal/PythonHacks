from django.urls import path
from .views import YoutubeViewset


urlpatterns = [
    path('youtube/', YoutubeViewset.as_view()),
    path('youtube/<int:id>', YoutubeViewset.as_view())
]