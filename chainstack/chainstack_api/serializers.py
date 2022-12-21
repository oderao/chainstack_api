from rest_framework import serializers
from .models import NewsItem

class NewsItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsItem
        fields = ('id','by','descendants','kids','score',
                  'date_created','title','story_type','url')