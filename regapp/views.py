from django.shortcuts import render
from django.contrib.auth.models import User
from regapp.serializers import StudentSerializer
from rest_framework.response import Response
from rest_framework import ISO_8601, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from . models import *
from . serializers import *

# Create your views here
#signup auth user
@api_view(['POST'])
def signup(request):
    if request.method=='POST':
        try:
            username=request.data['username']
            if User.objects.filter(username=username):
                return Response({'app_data':'user already exsisting','dev_data':'user is already exsisting'},status=status.HTTP_400_BAD_REQUEST)
            
        except:
            return Response({'app_data':'username is required','dev_data':'key name username is missing'},status=status.HTTP_400_BAD_REQUEST)
        try:
            password=request.data['password']
        except:
            return Response({'app_data':'password is required','dev_data':'key name password is missing'},status=status.HTTP_400_BAD_REQUEST)

        
        data=User.objects.create_user(
            username=username,
            password=password)
        data.save()
        profile=Profile(user=data)#add user object to profile
        profile.save()
        #get jwttoken 
        refresh = RefreshToken.for_user(profile)
        data ={}
        data.update({'refresh_token':str(refresh)})
        data.update({'access_token':str(refresh.access_token)})

             
        #response with jwttoken        
    return Response({'app_data':'success','dev_data':'successfully created','data':data},status=status.HTTP_201_CREATED)
#login with auth user
@api_view(['POST'])
def userlogin(request):
    if request.method=='POST':
        try:
            username=request.data['username']
            password=request.data['password']
            if User.objects.filter(username = username).exists():
                user=User.objects.get(username=username)
                print(user)
                pass
            else:
                return Response({'app_data':'This Email has not been registered. Please signup to continue','dev_data':'This email deosnot exists'}, status = status.HTTP_400_BAD_REQUEST)
            user=authenticate(username=username,password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                data = {}
                data.update({'refresh_token':str(refresh)})
                data.update({'access_token':str(refresh.access_token)})
                return Response({'app_data':'success','dev_data':'successfully created','data':data},status=status.HTTP_201_CREATED)
            else:
                return Response({'app_data':'failed','dev_data':'failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as E:
            return Response({'app_data':'Something went wrong', 'dev_data':str(E)}, status=status.HTTP_400_BAD_REQUEST)
#list data of auth user model
@permission_classes([IsAuthenticated])
@api_view(['GET'])            
def user_list(request):
 
    if request.method == 'GET':
        try:
            items = User.objects.all()
            items_serializer = StudentSerializer(items, many=True)
            return Response(items_serializer.data)
        except Exception as E:
            return Response({'app_data':'Something went wrong', 'dev_data':str(E)}, status=status.HTTP_400_BAD_REQUEST) 

#all user list with following and follower list

@api_view(['GET'])            
def allUser_follow_list(request):
 
    if request.method == 'GET':
        try:
            profiles = Profile.objects.all()
            items_serializer = ProfileSerializer(profiles, many=True)
            return Response(items_serializer.data)
        except Exception as E:
            return Response({'app_data':'Something went wrong', 'dev_data':str(E)}, status=status.HTTP_400_BAD_REQUEST) 

#for following anad follower
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def followinguser(request):
    if request.method=='POST':
        try:
            pid=request.data['id']
            print(pid)
            need_data= User.objects.get(id=pid) 
            print(need_data)
            current=request.user
            current_id=current.id
            print(current_id)
            current_name=current.username
            print(current_name)
            get_user=Profile.objects.get(user=current_id)
            print(get_user)
            if not (current_id==pid):
                if get_user.follow_ing.filter(id=pid).exists():
                    user=User.objects.get(id=pid)
                    get_user.follow_ing.remove(user)

                    "remove user"
                    new_follower=User.objects.get(id=current_id)
                    follower_user_id=Profile.objects.get(user=pid)
                    follower_user_id.follow_er.remove(new_follower)

                    return Response({'app_data':'removed','dev_data':'removed'},status=status.HTTP_200_OK)
                else:
                    user=User.objects.get(id=pid)
                    get_user.follow_ing.add(user)

                    '''add follower'''

                    new_follower=User.objects.get(id=current_id)
                    follower_user_id=Profile.objects.get(user=pid)
                    follower_user_id.follow_er.add(new_follower)

                    return Response({'app_data':'you are followed','dev_data':'followed'},status=status.HTTP_201_CREATED)
            else:
                return Response({'app_data':'cant follow yourself','dev_data':'cant follow yourself'},status=status.HTTP_400_BAD_REQUEST)    
                    
        except Exception as E:
            return Response({'app_data':'Something went wrong', 'dev_data':str(E)}, status=status.HTTP_400_BAD_REQUEST)
@permission_classes([IsAuthenticated])
@api_view(['GET'])            
def follower_list(request):
 
    if request.method == 'GET':
        try:
            current_user=request.user
            current_user_id=current_user.id
            
           
            items = Profile.objects.get(user=current_user_id)
            items_serializer = ProfileSerializer(items)
            return Response(items_serializer.data)
        except Exception as E:
            return Response({'app_data':'Something went wrong', 'dev_data':str(E)}, status=status.HTTP_400_BAD_REQUEST) 