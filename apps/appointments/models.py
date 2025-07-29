from django.db import models
import uuid
from apps.patients.models import Patient
from apps.doctors.models import Doctor
from apps.users.models import User
from django.core.validators import RegexValidator

# Create your models here.
class Appointment(models.Model):
    class Meta:
        db_table='appointments'
        ordering = ['-created_at'] 
        
    GENDER_CHOICES = [
        ("male","Male"),
        ("female","Female")
    ]    
    phone_regex = RegexValidator(
    regex=r'^(\+8801|01)\d{9}$',
    message="ফোন নম্বর অবশ্যই '+8801xxxxxxxxx' অথবা '01xxxxxxxxx' ফরম্যাটে হতে হবে।"
    )  
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
        ('video', 'Video Call')
    ]
    STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
    ('completed', 'Completed'),
    ]
    PAYMENT_STATUS_CHOICES = [
    ('unpaid', 'Unpaid'),
    ('paid', 'Paid'),
    ('refunded', 'Refunded'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE, null=True, blank=True,related_name="appointment_as_patient") 
    patient_name= models.CharField(max_length=30)
    email = models.EmailField(max_length=30) 
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES)
    phone_number = models.CharField(validators=[phone_regex], max_length=14, blank=False,null=False) 
    appointment_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointment_as_doctor")
    specialization = models.CharField(max_length=30, choices=SPECIALIZATION_CHOICES)
    consultation_type = models.CharField(max_length=20, choices=CONSULTATION_TYPE, default='offline')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    reschedule_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_appointment')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_appointment')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)