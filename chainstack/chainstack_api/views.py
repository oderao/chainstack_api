
from rest_framework import permissions
from .models import NewsItem
from .serializers import NewsItemSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse



def create_news_item(request):
    """_summary_

    Args:
        request (_type_): http request object

    Returns:
        _type:Json response if news item was created successfully
    """
    try:
      
        permission_classes = [permissions.AllowAny]
    
        if request.method == 'POST':
            
            
            
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            body['created_via'] = 'api'
            #build data object
            body['id'] = generate_id()
            
            serializer = NewsItemSerializer(data=body)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'message':'News Item Created Successfully'}, safe=False,status=status.HTTP_201_CREATED)
        return JsonResponse({'message':'Request method most be POST'},status=status.HTTP_403_FORBIDDEN)
    except:
        return JsonResponse({"message":"Error creating news item please try again later"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   