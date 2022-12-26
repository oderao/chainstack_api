from django.urls import path,include
from rest_framework import routers

from . import views



app_name = "chainstack_api"
urlpatterns = [
    
    path('create_news', views.create_news_item),
    path('list_news',views.read_news),
    path('delete_news',views.delete_news),
    path('set_quota',views.set_rate_limit_for_user),
    path('create_user',views.create_user),
    path('delete_user',views.delete_user),
    path('list_users',views.list_users),
    path('create_admin',views.create_admin),
    path('get_auth_token/',views.generate_token)
    
    
]