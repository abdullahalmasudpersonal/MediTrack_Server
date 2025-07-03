# from apps.admins.utils import Admin
def generate_admin_id(prefix='A-MT', length=6):
    from apps.admins.models import Admin
    last_id = Admin.objects.count() + 1
    return f"{prefix}{str(last_id).zfill(length)}"
