import json,random,string
from rest_framework import permissions,status
from rest_framework.decorators import api_view
from .models import NewsItem,APIRequestTracker
from .serializers import NewsItemSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication



def generate_token(request):
    """Generate a token a user can use to authenticate api calls

    Args:
        user (string): user_email_address
        password (string): user_passwor

    Returns:
        _type_: List containing the token to use
    """
    user_email = request.GET.get('user_email')
    password = request.GET.get('password')
    if user_email and password:
        #check if user exists
        user = User.objects.filter(email=user_email)
        
        #verify password
        if user and user[0].check_password(password):
            #generate token to use
            token, created = Token.objects.get_or_create(user=user[0])
            return JsonResponse({'token':token.key}, safe=False,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'message':'user not found'}, safe=False,status=status.HTTP_404_NOT_FOUND)
            
    else:
        return JsonResponse({'message':'no user name or password in request'}, safe=False,status=status.HTTP_400_BAD_REQUEST)        
    
@csrf_exempt #to test via local host postman
@api_view(['POST'])
def create_news_item(request):
    """_summary_

    Args:
        request (_type_): http request object

    Returns:
        _type:Json response if news item was created successfully
    """
    try:
        if log_and_validate_request(request.user):
            if request.method == 'POST':
                body_unicode = request.body.decode('utf-8')
                context = {}
                body = json.loads(body_unicode)
                request_user = User.objects.filter(username=request.user)
                if request_user:
                    context = {'created_by':request_user[0]}
                #build data object
                #body['id'] = generate_id()
                serializer = NewsItemSerializer(data=body,context=context)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'message':'News Item Created Successfully'}, safe=False,status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'message':'Request method must be POST'},status=status.HTTP_403_FORBIDDEN) #enforce post request for creation of news item
        else:
            return JsonResponse({'message':'Rate limit exceeded'},status=status.HTTP_403_FORBIDDEN) #enforce rate limit
            
    except Exception as e:
        print(e)
        return JsonResponse({"message":"Error creating news item please try again later"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
   
def generate_id():
    """generate random id for News Item"""
   
    ref = ''.join(random.choices(string.digits, k = 8))
    return ref 



def log_and_validate_request(user):
    """Log all api requests and validate request limits

    Args:
        user (_type_): user making the request
    """
    #NOTE Anon user rate limit is controlled is the django settings
    #check if log exists
    request_tracker = APIRequestTracker.objects.filter(user=user)
    if request_tracker:
        #check current_request_counter 
        request_tracker = request_tracker[0]
        if request_tracker.request_limit == 0: #0 is default means no rate limit has been set yet
            return True
        if request_tracker.current_request_count >= request_tracker.request_limit:
            return False
        else: #update current request_count
            request_tracker.current_request_count +=1
            request_tracker.save()
            return True
    else: #create a new tracker object
        #get user instance
        user = User.objects.filter(username=user)
        user = user[0]
        request_tracker = APIRequestTracker.objects.create(**{'user':user,'current_request_count':1})
        request_tracker.save()
        return True
        
            
def update_news_item(request):
    pass

def delete_news(request):
    pass

def read_news(request):
    pass

