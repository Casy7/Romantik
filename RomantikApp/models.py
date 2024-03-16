from re import T
from django.db import models
from django.contrib.auth.models import User
from traitlets import default
# Create your models here.

class NewsPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, auto_created=True)
    content = models.TextField(max_length=30000, blank=True)
    img_paths = models.JSONField(blank=True)

    was_updated = models.BooleanField(default=False)
    last_update = models.DateTimeField(blank=True, null=True)

    
class UpVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(NewsPost, on_delete=models.CASCADE)

class DownVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(NewsPost, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news_post = models.ForeignKey(NewsPost, on_delete=models.CASCADE)
    content = models.TextField(max_length=30000, blank=True)
    datetime = models.DateTimeField(auto_now_add=True, auto_created=True)

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(max_length=30000, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=25, blank=True)
    telegram = models.CharField(max_length=35, blank=True)

    is_email_public = models.BooleanField(default=False)
    is_phone_public = models.BooleanField(default=False)
    is_telegram_public = models.BooleanField(default=False)   

class Tag(models.Model):
    name = models.CharField(max_length=35)

class PostTag(models.Model):
    post = models.ForeignKey(NewsPost, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class TelegramChannelParserData(models.Model):
    channel = models.CharField(max_length=45, default="my_awesome_channel")
    last_post_id = models.IntegerField()
    last_update = models.DateTimeField(auto_now_add=True, auto_created=True)