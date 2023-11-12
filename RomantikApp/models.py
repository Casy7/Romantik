from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class NewsPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, auto_created=True)
    content = models.TextField(max_length=30000, blank=True)
    img_paths = models.JSONField(blank=True)
    
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
    avatar = models.ImageField(upload_to='images/', null=True, blank=True)