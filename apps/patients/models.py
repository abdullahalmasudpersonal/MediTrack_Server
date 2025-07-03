from django.db import models
from django.core.validators import RegexValidator
import uuid
from apps.users.models import User

# Create your models here.
class Patient(models.Model):
    class Meta:
        db_table='patients'
        # ordering = ['-created_at'] 
        
    phone_regex = RegexValidator(
    regex=r'^(\+8801|01)\d{9}$',
    message="ফোন নম্বর অবশ্যই '+8801xxxxxxxxx' অথবা '01xxxxxxxxx' ফরম্যাটে হতে হবে।"
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    user =  models.OneToOneField(User,on_delete=models.CASCADE,related_name="patient_profile")    
    name = models.CharField(max_length=30)
    age = models.PositiveIntegerField(blank=True, null=True)
    birthDate = models.DateField(blank=False, null=False)
    patientPhoto = models.ImageField(upload_to='patient_photos/', blank=True, null=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=False,null=False)
    address = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)    
    