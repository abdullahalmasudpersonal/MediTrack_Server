from django.db import models
import uuid

# Create your models here.
class Service(models.Model):
    class Meta:
        db_table = 'services'
        ordering = ['-created_at'] 
        
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
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)     
    name = models.CharField(max_length=50, unique=True) 
    category = models.CharField(max_length=30, choices=SPECIALIZATION_CHOICES,unique=True)
    short_description=models.TextField(max_length=500,blank=True, null=True)
    description=models.TextField(max_length=4000,blank=True, null=True)
    description2=models.TextField(max_length=4000,blank=True, null=True)
    image=models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True) 
    