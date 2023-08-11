from .views import *
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("news/", NewsPage.as_view(), name="news"),
    path("signin/", Login.as_view(), name="login"),
    path("signout/", Logout.as_view(), name="logout"),
    path("signup/", SignUp.as_view(), name="registration"),
    re_path('publish_post/', AjaxPublishPost.as_view(), name='publish_post'),
    re_path('add_photo_to_news_post/', AjaxAddPhotoToPost.as_view(), name='add_photo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)