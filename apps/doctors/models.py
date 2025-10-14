from django.db import models
import uuid
from django.core.validators import RegexValidator
from apps.users.models import User

# Create your models here.
class Doctor(models.Model):
    class Meta:
        db_table = 'doctors'
        
    phone_regex = RegexValidator(
    regex=r'^(\+8801|01)\d{9}$',
    message="ফোন নম্বর অবশ্যই '+8801xxxxxxxxx' অথবা '01xxxxxxxxx' ফরম্যাটে হতে হবে।"
    )
    
    GENDER_CHOICES = [
        ("male","Male"),
        ("female","Female")
    ]
    
    SPECIALIZATION_CHOICES = [
    ('cardiology', 'Cardiology'),
    ('dermatology', 'Dermatology'),
    ('neurology', 'Neurology'),
    ('pediatrics', 'Pediatrics'),
    ('orthopedics', 'Orthopedics'),
    ('gynecology', 'Gynecology'),
    ('psychiatry', 'Psychiatry'),
    ('general', 'General Medicine'),
    ('surgery', 'Surgery'),
    ('radiology', 'Radiology'),
    ('ent', 'ENT (Ear, Nose, Throat)'),
    ('urology', 'Urology'),
    ('oncology', 'Oncology'),
    ('ophthalmology', 'Ophthalmology'),
    ('anesthesiology', 'Anesthesiology'),
    ]
 
    CONSULTATION_TYPE = [
        ('online', 'Online'), 
        ('offline', 'Offline'), 
    ]
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    user =  models.OneToOneField(User,on_delete=models.CASCADE,related_name="doctor_profile")  
    name = models.CharField(max_length=30, unique=True) 
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=False,null=False)  
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES)
    birthDate = models.DateField(blank=True, null=True)
    specialization = models.CharField(max_length=30, choices=SPECIALIZATION_CHOICES)
    license_number = models.CharField(max_length=50, unique=True,blank=True, null=True )
    education = models.TextField(blank=True, null=True,max_length=80)
    experience_years = models.PositiveIntegerField(blank=True, null=True )
    hospital_affiliation = models.CharField(max_length=100, blank=True, null=True)
    availability = models.JSONField(blank=True, null=True)  # Example: {"monday": "10am-5pm"}
    fees = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    photo = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=50,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True) 