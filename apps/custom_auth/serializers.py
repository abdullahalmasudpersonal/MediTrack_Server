
from rest_framework import serializers
from apps.users.models import User

class UserLimitedSerializer(serializers.ModelSerializer):
    profile_id = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'email', 'role','profile_id']

    def get_profile_id(self, obj):
        from apps.admins.models import Admin
        from apps.doctors.models import Doctor
        from apps.patients.models import Patient

        try:
            if obj.role == 'admin':
                return str(Admin.objects.get(user=obj).id)
            elif obj.role == 'doctor':
                return str(Doctor.objects.get(user=obj).id)
            elif obj.role == 'patient':
                return str(Patient.objects.get(user=obj).id)
        except:
            return None

