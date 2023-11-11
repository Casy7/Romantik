from django import urls
from .views import *
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("news/", NewsPage.as_view(), name="news"),
    path('hikes/', Hikes.as_view(), name="hikes"),
    path("signin/", Login.as_view(), name="login"),
    path("signout/", Logout.as_view(), name="logout"),
    path("signup/", SignUp.as_view(), name="registration"),
    path("about/", AboutUs.as_view(), name="about_us"),
    path("rules/", Rules.as_view(), name="rules"),
    path("old_rules/", OldRules.as_view(), name="old_rules"),
    path("history/", History.as_view(), name="history"),
    path("contacts/", Contacts.as_view(), name="contacts"),
    path("hymn/", Hymn.as_view(), name="hymn"),
    path("post/<int:post_id>", FullPost.as_view(), name="full_post"),

    re_path('vote_post/', AjaxVotePost.as_view(), name='vote_post'),
    re_path('publish_post/', AjaxPublishPost.as_view(), name='publish_post'),
    re_path('add_photo_to_news_post/', AjaxAddPhotoToPost.as_view(), name='add_photo'),
    re_path('publish_comment/', AjaxPublishComment.as_view(), name='publish_comment'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'RomantikApp.views.handler404'