from django.contrib import admin

# Register your models here.

from .models import NewsItem,APIRequestTracker



class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("news_id","title")
    

admin.site.register(NewsItem,NewsItemAdmin)
admin.site.register(APIRequestTracker)
