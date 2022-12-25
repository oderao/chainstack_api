from django.urls import path,include
from rest_framework import routers

from . import views



app_name = "chainstack_api"
urlpatterns = [
    
    path('create_news', views.create_news_item),
    path('list_news',views.read_news),
    path('delete_news',views.delete_news),
    path('get_auth_token/',views.generate_token)
    
    
]