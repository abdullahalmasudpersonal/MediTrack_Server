from .models import Patient
def generate_patient_id(prefix='P-MT', length=6):
    last_id = Patient.objects.count() + 1
    return f"{prefix}{str(last_id).zfill(length)}"
