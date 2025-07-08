from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserRoles(models.TextChoices):
    """
    Create/Modify user roles here
    Add role in the same format (CUSTOM_ROLE = 'custom_role', 'Custom Role')
    """
    ADMIN = 'admin', 'Admin'
    DRIVER = 'driver', 'Driver'
    RIDER = 'rider', 'Rider'
    PARTNER = 'partner', 'Partner'

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        print(password + " IN BASEMANAGER")
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", UserRoles.ADMIN)
        return self.create_user(email, password, **extra_fields)
    

class User(AbstractBaseUser, PermissionsMixin):
    """
    User model representing different roles in the application.
    """
    id_user = models.AutoField(primary_key=True)
    role = models.CharField(max_length=10, choices=UserRoles)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
