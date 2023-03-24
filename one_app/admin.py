from django.contrib import admin
from .models import *


class MenuItemInline(admin.TabularInline):
    model = MenuItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'menu', 'otheritem']
    list_filter = ['menu']



