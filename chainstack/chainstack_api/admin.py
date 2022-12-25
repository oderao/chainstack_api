from django.contrib import admin

# Register your models here.

from .models import NewsItem,APIRequestTracker

admin.site.register(NewsItem)
admin.site.register(APIRequestTracker)
