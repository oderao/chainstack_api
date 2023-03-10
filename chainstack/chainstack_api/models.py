from time import time
from turtle import title
from unittest.util import _MAX_LENGTH
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.
class NewsItem(models.Model):

    item_types = [
        ("job", "job"),
        ("story", "story"),
        ("comment", "comment"),
        ("poll", "poll"),
        ("pollopt", "pollopt"),
        ("", ""),
    ]

    news_id = models.CharField(
        primary_key=True, max_length=200
    )  # unique id of NewsItem
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    news_detail = models.TextField(null=True, max_length=1000)  # text summary of news
    date_created = models.DateTimeField(
        null=True
    )  # Creation date of the item in unix time
    title = models.CharField(
        max_length=300
    )  # The title of the news story, poll or job.
    story_type = models.CharField(
        null=True, max_length=10, choices=item_types, default=""
    )
    url = models.CharField(null=True, max_length=300)  # The URL of the story.

    # create date from timestap in unix

    def create_date_time(self, unix_time=""):
        if isinstance(unix_time, str):
            unix_time = float(unix_time)

        converted_date = datetime.fromtimestamp(unix_time)
        return converted_date

    def __str__(self):
        return self.title


class APIRequestTracker(models.Model):

    user = models.ForeignKey(User, primary_key=True, on_delete=models.CASCADE)
    request_limit = models.PositiveIntegerField(default=0)
    current_request_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.user)


class ErrorLog(models.Model):

    log = models.TextField(null=True, editable=True)
    log_view = models.CharField(null=True, max_length=100)
    log_id = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.log_id)
