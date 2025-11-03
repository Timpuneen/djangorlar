from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    """First approach to a custom user model."""
    phone_number = models.CharField(max_length=15, blank=True, null=True,verbose_name="Phone Number xdd")
    date_of_birth = models.DateField(blank=True, null=True,verbose_name="Date of Birth xdd")
    bio = models.TextField(blank=True, null=True,verbose_name="Bio xdd")
    location = models.CharField(max_length=100, blank=True, null=True,verbose_name="Location xdd")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Created At xdd")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Updated At xdd")

    class Meta:
        verbose_name = "Custom User xdd"
        verbose_name_plural = "Custom Users xdd"
        
    def __str__(self):
        return self.username
    
# class CustomUserFullManager(BaseUserManager):
#     """Manager for CustomUserFull."""
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(email, password, **extra_fields)
    
class CustomUserFull(AbstractBaseUser, PermissionsMixin):
    """Second approach to a custom user model with email as username."""
    email = models.EmailField(unique=True,verbose_name="Email xdd")
    first_name = models.CharField(max_length=30, blank=True,verbose_name="First Name xdd")
    last_name = models.CharField(max_length=30, blank=True,verbose_name="Last Name xdd")
    phone_number = models.CharField(max_length=15, blank=True, null=True,verbose_name="Phone Number xdd")
    date_of_birth = models.DateField(blank=True, null=True,verbose_name="Date of Birth xdd")
    bio = models.TextField(blank=True, null=True,verbose_name="Bio xdd")
    location = models.CharField(max_length=100, blank=True, null=True,verbose_name="Location xdd")
    is_active = models.BooleanField(default=True,verbose_name="Is Active xdd")
    is_staff = models.BooleanField(default=False,verbose_name="Is Staff xdd")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Created At xdd")
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Updated At xdd")

    objects = CustomUserFullManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Custom User Full xdd"
        verbose_name_plural = "Custom Users Full xdd"
        
    def __str__(self):
        return self.email