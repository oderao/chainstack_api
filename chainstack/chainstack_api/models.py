from time import time
from turtle import title
from unittest.util import _MAX_LENGTH
from django.db import models
from datetime import datetime


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
    news_type_ = [
                    ('auto','auto'),
                    ('api','api'),
                    ]
    
    by =  models.CharField(null=True,max_length=200) #The username of the item's author
    descendants = models.IntegerField(null=True) #In the case of stories or polls, the total comment count.
    id = models.IntegerField(primary_key=True,null=False) #The item's unique id
    kids = models.CharField(null=True,max_length=400) #The ids of the item's comments, in ranked display order.
    score = models.PositiveIntegerField(null=True) #The story's score, or the votes for a pollopt
    date_created = models.DateTimeField(null=True) #Creation date of the item in unix time
    title = models.CharField(null=True,max_length=300) #The title of the story, poll or job.
    story_type = models.CharField(null=True,max_length=10,choices=item_types,default='')
    url = models.CharField(null=True,max_length=300) #The URL of the story.
    created_via = models.CharField(null=True,max_length=10,choices=news_type_,default='')#defines the way the news was created auto or via api


    #create date from timestap in unix
    
    def create_date_time(self,unix_time=''):
        if isinstance(unix_time,str):
            unix_time = float(unix_time)
            
        converted_date = datetime.fromtimestamp(unix_time)
        return converted_date
        
        
    
    
    
    def __str__(self):
        return self.title