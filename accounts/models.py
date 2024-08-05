from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
   
    phone=models.CharField( max_length=50)
    kayphone=models.CharField(max_length=8,default='+967')
    def __str__(self):
        return  self.user.username