from django.contrib import admin
from .models import *
# Register your models here.


class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime')
    search_fields = ('user', 'datetime')  # Fields to search in the list view


admin.site.register(NewsPost, NewsPostAdmin)

class UpVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'news')

admin.site.register(UpVote, UpVoteAdmin)

class DownVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'news')

admin.site.register(DownVote, DownVoteAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'news_post', 'datetime', 'content')
    search_fields = ('user', 'news_post', 'datetime') 

admin.site.register(Comment, CommentAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'phone', 'telegram')
    search_fields = ('user', 'email', 'phone', 'telegram')

admin.site.register(UserInfo, UserProfileAdmin)