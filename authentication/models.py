from django.db import models
from django.contrib.auth.models import AbstractUser



class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    full_name = models.CharField(max_length=200, null=True, blank=False)
    email = models.EmailField(unique=True, null=True, blank=False)
    is_admin = models.BooleanField(default=False)
    is_registry = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=False)
    
    class Meta:
        ordering = ['username']
    
    def __str__(self):
        return self.username

