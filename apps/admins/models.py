from django.db import models
import uuid
from django.core.validators import RegexValidator

# Create your models here.
class Admin(models.Model):
    class Meta:
        db_table='admins'
        
    phone_regex = RegexValidator(
    regex=r'^(\+8801|01)\d{9}$',
    message="ফোন নম্বর অবশ্যই '+8801xxxxxxxxx' অথবা '01xxxxxxxxx' ফরম্যাটে হতে হবে।"
    )
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    userId = models.CharField(max_length=10, unique=True)   
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, unique=True) 
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=False,null=False) 
    address = models.TextField(blank=True, null=True)
    patientPhoto = models.ImageField(upload_to='patient_photos/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True) 