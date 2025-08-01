# Generated by Django 5.2 on 2025-07-30 11:28

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('phone_number', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message="ফোন নম্বর অবশ্যই '+8801xxxxxxxxx' অথবা '01xxxxxxxxx' ফরম্যাটে হতে হবে।", regex='^(\\+8801|01)\\d{9}$')])),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=30)),
                ('birthDate', models.DateField(blank=True, null=True)),
                ('specialization', models.CharField(choices=[('cardiology', 'Cardiology'), ('dermatology', 'Dermatology'), ('neurology', 'Neurology'), ('pediatrics', 'Pediatrics'), ('orthopedics', 'Orthopedics'), ('gynecology', 'Gynecology'), ('psychiatry', 'Psychiatry'), ('general', 'General Medicine'), ('surgery', 'Surgery'), ('radiology', 'Radiology'), ('ent', 'ENT (Ear, Nose, Throat)'), ('urology', 'Urology'), ('oncology', 'Oncology'), ('ophthalmology', 'Ophthalmology'), ('anesthesiology', 'Anesthesiology')], max_length=30)),
                ('license_number', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('education', models.TextField(blank=True, max_length=80, null=True)),
                ('experience_years', models.PositiveIntegerField(blank=True, null=True)),
                ('hospital_affiliation', models.CharField(blank=True, max_length=100, null=True)),
                ('availability', models.JSONField(blank=True, null=True)),
                ('consultation_type', models.CharField(choices=[('online', 'Online'), ('offline', 'Offline'), ('video', 'Video Call')], default='offline', max_length=20)),
                ('fees', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('photo', models.URLField(blank=True, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_profile', to='users.user')),
            ],
            options={
                'db_table': 'doctors',
            },
        ),
    ]
