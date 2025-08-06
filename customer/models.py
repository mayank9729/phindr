import datetime
from django.db import models
import random
import string
import uuid 
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from core.utils.common import Common

# Random String Generate
random_string = ''.join(random.choices(string.ascii_uppercase +string.digits, k=7))

class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Must have a email address.")
        user = self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Customer
class User(AbstractBaseUser,PermissionsMixin):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('admin', 'Admin'),
        ('seller', 'Seller'),
    )
    first_name  =   models.CharField(max_length=50,blank=True,null=True)
    last_name   =   models.CharField(max_length=50,blank=True,null=True)
    email       =   models.EmailField(max_length=50,unique=True,null=True,blank=True)
    phone       =   models.CharField(unique=True,max_length=13,blank=True,null=True)
    is_active   =   models.BooleanField(default=True)
    is_staff    =   models.BooleanField(default=False)
    is_admin    =   models.BooleanField(default=False)
    role        =   models.CharField(max_length=20, choices=ROLE_CHOICES, default='buyer')
    unique_id   =   models.CharField(max_length=8,default=uuid.uuid4().hex[:6].upper())
    update_at   =   models.DateField(default=datetime.date.today)
    created_at  =   models.DateField(default=datetime.date.today)
    profile_image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    objects     =   UserManager()
    token       =   models.CharField(max_length=100,blank=True,null=True)

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'customer'
        verbose_name = ("Customer")
        
class IPAddress(models.Model):
    ip = models.GenericIPAddressField(null=True,blank=True)
    is_blocked=models.BooleanField(default=False)