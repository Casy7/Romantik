from django.contrib import admin

from .models import *

class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'cathegory', 'price', 'amount')
    search_fields = ('name', 'cathegory', 'price', 'amount')

admin.site.register(Equipment, EquipmentAdmin)

class CathegoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_cathegory')
    search_fields = ('name', 'parent_cathegory')

admin.site.register(Cathegory, CathegoryAdmin)