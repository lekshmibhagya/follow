from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username')
class ProfileSerializer(serializers.ModelSerializer):
    follow_er= StudentSerializer(read_only=True, many=True)
    follow_ing= StudentSerializer(read_only=True,many=True)
    class Meta:
        model=Profile
        fields=('user','follow_er',"follow_ing")
    

