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
    path("my_account/", AccountEditor.as_view(), name="my_account"),
    path("about/", AboutUs.as_view(), name="about_us"),
    path("rules/", Rules.as_view(), name="rules"),
    path("old_rules/", OldRules.as_view(), name="old_rules"),
    path("old_rules_ukr/", OldRulesUkr.as_view(), name="old_rules_ukr"),	
    path("history/", History.as_view(), name="history"),
    path("contacts/", Contacts.as_view(), name="contacts"),
    path("hymn/", Hymn.as_view(), name="hymn"),
    path("post/<int:post_id>", FullPost.as_view(), name="full_post"),
    path("post/<int:post_id>/edit", PostEditor.as_view(), name="edit_post"),
	path("user/<str:username>", UserProfile.as_view(), name="user_page"),
	
    path('get_posts_from_tg/', AjaxGetNewsFromTelegramUpdater.as_view(), name='get_posts_from_tg'),
	path('load_more_posts/', AjaxLoadMorePosts.as_view(), name='load_more_posts'),
    path('vote_post/', AjaxVotePost.as_view(), name='vote_post'),
    path('publish_post/', AjaxPublishPost.as_view(), name='publish_post'),
    path('update_post/', AjaxUpdatePost.as_view(), name='update_post'),
    path('add_photo_to_news_post/', AjaxAddPhotoToPost.as_view(), name='add_photo'),
    path('publish_comment/', AjaxPublishComment.as_view(), name='publish_comment'),
	path('upload_user_avatar/', AjaxUploadUserAvatar.as_view(), name='upload_user_avatar'),
	
    path('robots.txt', ReturnRobotsTxt.as_view(), name='robots_txt'),
	path('sitemap.xml', GetSitemap.as_view(), name='sitemap_xml'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'RomantikApp.views.handler404'