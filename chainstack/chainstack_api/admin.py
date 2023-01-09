from django.contrib import admin

# Register your models here.

from .models import NewsItem, APIRequestTracker, ErrorLog


class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("news_id", "title")


class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ("log_id", "log_view", "date_created")


admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(APIRequestTracker)
admin.site.register(ErrorLog, ErrorLogAdmin)
