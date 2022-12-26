from rest_framework import serializers
from .models import NewsItem
from django.contrib.auth.models import User


class NewsItemSerializer(serializers.ModelSerializer):
    
    
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    
    
    #modify create function to save foreign key created by
    def create(self, validated_data):
        if self.context['created_by']:
            created_by = self.context['created_by']
            validated_data['created_by'] = created_by
        post = NewsItem.objects.create(**validated_data)  # saving News object
        return post
    
    class Meta:
        model = NewsItem
        fields = ('news_id',"created_by",
                  'date_created','title','url','story_type','news_detail')
        
