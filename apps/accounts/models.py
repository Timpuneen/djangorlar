from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    """Manager for CustomUser."""
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractUser):
    """Custom user model extending AbstractUser."""
    
    DEPARTMENT_CHOICES = [
        ('IT', 'IT'),
        ('HR', 'HR'),
        ('Sales', 'Sales'),
        ('Finance', 'Finance'),
    ]
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]
    
    email = models.EmailField(unique=True, verbose_name='Email')
    
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Phone')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='City')
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name='Country')
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, blank=True, null=True, verbose_name='Department')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, null=True, verbose_name='Role')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Birth Date')
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Salary')
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    def __str__(self):
        return self.email