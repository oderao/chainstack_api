from time import time
from turtle import title
from unittest.util import _MAX_LENGTH
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.
class NewsItem(models.Model):
    
    item_types = [
                    ('job','job'),
                    ('story','story'),
                    ('comment','comment'),
                    ('poll','poll'),
                    ('pollopt','pollopt'),
                    ('','')
                    ]
    
    by =  models.CharField(null=True,max_length=200) #The username of the item's author
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    #descendants = models.IntegerField(null=True) #In the case of stories or polls, the total comment count.
    #id = models.IntegerField(primary_key=True,null=False) #The item's unique id
    date_created = models.DateTimeField(null=True) #Creation date of the item in unix time
    title = models.CharField(primary_key =True,max_length=300) #The title of the story, poll or job.
    story_type = models.CharField(null=True,max_length=10,choices=item_types,default='')
    url = models.CharField(null=True,max_length=300) #The URL of the story.

    #create date from timestap in unix
    
    def create_date_time(self,unix_time=''):
        if isinstance(unix_time,str):
            unix_time = float(unix_time)
            
        converted_date = datetime.fromtimestamp(unix_time)
        return converted_date
        
        
    
    
    
    def __str__(self):
        return self.title
    
class APIRequestTracker(models.Model):
    
    user = models.ForeignKey(User,unique=True, on_delete=models.CASCADE)
    request_limit = models.PositiveIntegerField(default=0)
    current_request_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return str(self.user)