
from django.urls import path
from .views import WeatherList,Corn_grain_yieldList,DataAnalysisList

urlpatterns = [
    path("weather",WeatherList.as_view()),
    path("yield",Corn_grain_yieldList.as_view()),
    path("weather/stats",DataAnalysisList.as_view()),
]