from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,PermissionsMixin
from .manager import CustomUserManager
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email_address'), unique=True)
    # phone = models.CharField(help_text='Contact phone number', unique=True,max_length=10)
    phone = models.CharField(help_text='Contact phone number', unique=True, max_length=20, null=True, blank=True)

    image = models.ImageField(upload_to='images/', blank=True, null=True)
   
    
    def __str__(self):
        return self.first_name

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
