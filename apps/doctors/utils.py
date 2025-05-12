from .models import Doctor
def generate_doctor_id(prefix='D-MT', length=6):
    last_id = Doctor.objects.count() + 1
    return f"{prefix}{str(last_id).zfill(length)}"
