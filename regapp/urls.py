from django.urls import path
from . import views

urlpatterns=[
    path('signup/',views.signup,name='signup'),
    path('userlogin/',views.userlogin,name='userlogin'),
    path('user_list/',views.user_list,name='user_list'),
    path('follower_list/',views.follower_list,name='follower_list'),
    path('followinguser/',views.followinguser,name='followinguser'),
    path('allUser_follow_list/',views.allUser_follow_list,name='allUser_follow_list')
]