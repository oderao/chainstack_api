from django.contrib import admin

# Register your models here.

from .models import NewsItem

admin.site.register(NewsItem)
