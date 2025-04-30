from django.contrib import admin
from .models import User
from django.utils import timezone

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "userId", "email", "password", "role", "status", "created_at", "updated_at","is_deleted"]

