from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class NewsPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, auto_created=True)
    content = models.TextField(max_length=30000, blank=True)
    img_paths = models.JSONField(blank=True)
    
