from .models import Admin
def generate_admin_id(prefix='A-MT', length=6):
    last_id = Admin.objects.count() + 1
    return f"{prefix}{str(last_id).zfill(length)}"
