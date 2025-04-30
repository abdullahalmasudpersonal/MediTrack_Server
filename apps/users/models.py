from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    class Meta:
        db_table = 'users' 
        ordering = ['-created_at'] 
        
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    ROLE_CHOICES = [
        ('admin','Admin'),
        ('doctor','Doctor'),
        ('patient','Patient')
    ]

    userId = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=30, unique=True)  
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES,default='patient')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
    # যদি password hash করা না থাকে তাহলে hash করে দাও
     if not self.password.startswith('pbkdf2_'):
        self.password = make_password(self.password)
     super().save(*args, **kwargs)