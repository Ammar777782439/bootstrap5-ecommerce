from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="userprofile")
    phone = models.CharField(max_length=50)
    kayphone = models.CharField(max_length=8, default='+967')
    image = models.ImageField(upload_to='accounts/%y/%m/%d', default='accounts/24/07/29/home4.png')
    
    
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username
