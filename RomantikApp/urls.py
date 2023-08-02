from .views import *
from django.urls import path, re_path

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("news/", NewsPage.as_view(), name="news"),
    path("signin/", Login.as_view(), name="login"),
    path("signout/", Logout.as_view(), name="logout"),
    path("signup/", SignUp.as_view(), name="registration"),
    re_path('publish_post/', AjaxPublishPost.as_view(), name='publish_post'),
]