from .views import *
from django.urls import path

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("news/", NewsPage.as_view(), name="news"),
]