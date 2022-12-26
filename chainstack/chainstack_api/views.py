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
                body['news_id'] = generate_id()
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
   
    ref = ''.join(random.choices(string.digits+string.ascii_uppercase, k = 8))
    return ref 



def log_and_validate_request(user,rate_limit=0):
    """Log all api requests and validate request limits

    Args:
        user (_type_): user making the request
    """
    #NOTE Anon user rate limit is controlled is the django settings
    #superuser shouldnt be rate limited
    
    user_object = User.objects.filter(username=user)
    
    if user and user_object[0].is_superuser:
        return True
    # #check if log exists
    
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


@api_view(['DELETE'])
def delete_news(request):
    """delete news item by its id"""
    try:      
      if request.method == "DELETE":
         body_unicode = request.body.decode('utf-8')
         body = json.loads(body_unicode)
         if body.get('news_id'):
            item = NewsItem.objects.get(pk=body.get("news_id"))
            if item and item.created_by == request.user: #user should delete only resources they create
               item.delete()
               return JsonResponse({'message':'News Item deleted'},status=status.HTTP_200_OK)
               
            else:
               return JsonResponse({'message':'News Item does not exist in database or you dont have permission to delete'},status=status.HTTP_417_EXPECTATION_FAILED)
               
         else:
            return JsonResponse({'message':'No news_id in request data'},status=status.HTTP_417_EXPECTATION_FAILED)
      return JsonResponse({'message':'Request method must be DELETE'},status=status.HTTP_403_FORBIDDEN)

    except NewsItem.DoesNotExist:
      return JsonResponse({"message":"Error deleting news item please try again later",
                           "error":"News Item Does not exist"
                           },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def read_news(request):
    """retrieve news items created by single user or all by superuser """
    try: 
        if request.method == 'GET':
            #check if user is superuser ie admin
            user = User.objects.filter(username=request.user)
            if user and user[0].is_superuser:
                pass
                news_list = NewsItem.objects.all().order_by('-date_created')
            else:
                news_list = NewsItem.objects.all().filter(created_by=request.user).order_by('-date_created')
                        
            news_list_data = NewsItemSerializer(news_list, many=True)
            
            if news_list_data.data:
                return JsonResponse(news_list_data.data, safe=False)
            return JsonResponse({"message":"No news available"},safe=False,status=status.HTTP_404_NOT_FOUND)
    except:
        return JsonResponse({"message":"Error creating listing news items please try again later"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(['POST'])
def create_user(request,*args,**kwargs):
    """Create userS on the backend

    Args:
        request (_type_): http request object
    """
    try:
        user_dict = {}
        password = request.GET.get('password')
        username = request.GET.get('username')
        email = request.GET.get('email')
        superuser = request.GET.get('superuser',0)
        if username and password and email:
            user_dict.update({
                'password':password,
                'username':username,
                'email':email,
                'is_superuser':superuser
            })
            #create user
            user_model = User.objects.create(**user_dict)
            user_model.save()
            return JsonResponse({'message':'User Created',
                                 'user_details':user_dict},status=status.HTTP_201_CREATED)
            
        else:
            return JsonResponse({'message':'Username,password and email are manadatory parameters'},status=status.HTTP_417_EXPECTATION_FAILED)
    except:
        return JsonResponse({'message':'Error creating user please try again later'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        
    
    
    
@api_view(['DELETE'])
def delete_user(request):
    """delete user by its given usrname"""
    try:
        username = request.GET.get('username')
        if username:
            user_model = User.objects.get(username=username)
            user_model.delete()
            return JsonResponse({'message':'User Deleted'},status=status.HTTP_200_OK)
            
        else:
            return JsonResponse({'message':'No username in request parameter'},status=status.HTTP_417_EXPECTATION_FAILED)
            
    except:
        return JsonResponse({'message':'Error deleting user please try again later'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(['GET'])
def list_users(request):
    """get a list of all users on the system"""
    try:
        if check_superuser(request.user):
            
            user_list = User.objects.all().values('username','email','is_superuser','date_joined').order_by('-username')
            if user_list:
                user_list = list(user_list)
                return JsonResponse({'data':user_list}, safe=False)
            return JsonResponse({'message':'No users in db'},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return JsonResponse({'message':'Error listing users please try again later'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    
    
@api_view(['PUT'])
def set_rate_limit_for_user(request):
    """Set rate limit for user

    Args:
        request (_type_): http request object
    """
    #check if request tracker already exists for user
    try:
        request_limit = request.GET.get('request_limit',0)
        user = request.GET.get('user')
        if user and User.objects.filter(username=user):
            #get user instance
            user_model = User.objects.filter(username=user)
            if user_model and user_model[0].is_superuser:
                return JsonResponse({"message":"superuser has no limit"},safe=False,status=status.HTTP_404_NOT_FOUND)
                
        
            #check if tracker already exists
            request_tracker = APIRequestTracker.objects.filter(user=user_model[0])
            
            if request_tracker:
                #update tracker
                request_tracker[0].request_limit = request_limit
                request_tracker[0].save()
                return JsonResponse({"message":"rate limit set"},safe=False,status=status.HTTP_200_OK)
                
            else:
                request_tracker = APIRequestTracker.objects.create(**{'user':user_model[0],'request_limit':request_limit})
                request_tracker.save()
                return JsonResponse({"message":"Rate limit set"},safe=False,status=status.HTTP_201_CREATED)
                
        else:
            return JsonResponse({"message":"user does not exist"},safe=False,status=status.HTTP_404_NOT_FOUND)
    except:
        return JsonResponse({"message":"Error setting quota please try again later"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

def check_superuser(user):
    
    """Helper function to validate views that require superuser ie platform admin"""
    
    user_model = User.objects.filter(username=user)
    if user_model and user_model[0].is_superuser:
        return True
    else:
        return False
        
        