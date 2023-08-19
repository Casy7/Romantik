from django.contrib import admin
from .models import *
# Register your models here.


class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime')
    list_display = ('user', 'datetime')  # Fields to display in the list view
    search_fields = ('user', 'datetime')  # Fields to search in the list view


admin.site.register(NewsPost, NewsPostAdmin)

class UpVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'news')

admin.site.register(UpVote, UpVoteAdmin)

class DownVoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'news')

admin.site.register(DownVote, DownVoteAdmin)