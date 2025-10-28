from django.db import models
import uuid
from apps.doctors.models import Doctor

# Create your models here.
class Schedule(models.Model):
    class Meta:
        db_table='schedules'
        unique_together = ('doctor', 'weekday', 'start_time', 'end_time')

    WEEKDAYS = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    weekday = models.IntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active= models.BooleanField(default=True)

    # def __str__(self):
    #     return f"{self.doctor.name} - {self.get_weekday_display()} ({self.start_time}-{self.end_time})"