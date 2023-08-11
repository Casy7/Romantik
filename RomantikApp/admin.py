from django.contrib import admin
from .models import NewsPost
# Register your models here.


class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime')
    list_display = ('user', 'datetime')  # Fields to display in the list view
    search_fields = ('user', 'datetime')  # Fields to search in the list view


admin.site.register(NewsPost, NewsPostAdmin)