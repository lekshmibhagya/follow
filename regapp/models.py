from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    follow_ing = models.ManyToManyField(User,related_name='follow_ing',blank=True)   
    follow_er = models.ManyToManyField(User,related_name='follow_er',blank=True)
    
