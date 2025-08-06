from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
import uuid

# Create your models here.
# class MasterData(models.Model):
#     TYPE_CHOICES = [
#         ('complaint_category', 'Complaint Category'),
#         ('visitor_purpose', 'Visitor Purpose'),
#         ('vehicle_type', 'Vehicle Type'),
#         ('id_proof_type', 'ID Proof Type'),
#         ('floor', 'Floor'),
#         ('status', 'Status'),
#         ('priority', 'Priority')
#     ]

#     VALUE_CHOICES = [
#         ('plumbing', 'Plumbing'),
#         ('electricity', 'Electricity'),
#         ('security', 'Security'),
#         ('cleaning', 'Cleaning'),
#         ('water_supply', 'Water Supply'),
#         ('parking', 'Parking'),
#         ('other', 'Other')
#     ]
#     type = models.CharField(max_length=50, choices=TYPE_CHOICES)
#     value = models.CharField(max_length=50, choices=VALUE_CHOICES)
#     display_order = models.IntegerField(default=0)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'master_data'

#     def __str__(self):
#         return self.value

class MasterType(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MasterValue(models.Model):
    type = models.ForeignKey(MasterType, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=100)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('type', 'value')
        ordering = ['type', 'display_order']

    def __str__(self):
        return self.value
    
class CustomUser(AbstractUser):
    username = None
    USER_TYPE_CHOICES = [
        ('owner', 'Owner'),
        ("tenent", 'Tenent')
    ]
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    owner_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=True, blank=True)
    mobile = models.CharField(max_length=13, unique=True)
    flat = models.CharField(max_length=4)
    bike_number = models.CharField(max_length=12, blank=True, null=True)
    car_number = models.CharField(max_length=12, blank=True, null=True)
    id_type = models.ForeignKey(MasterValue, on_delete=models.CASCADE, related_name='id_type', limit_choices_to={'type__code': 'id_proof_type'})
    id_number = models.CharField(max_length=50, unique=True)

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name

# models.py

class Complaint(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(MasterValue, on_delete=models.CASCADE, limit_choices_to={'type__code': 'complaint_category'}, related_name='complaint_type')
    priority = models.ForeignKey(MasterValue, on_delete=models.CASCADE, limit_choices_to={'type__code': 'priority'}, related_name='priority')
    status = models.ForeignKey(MasterValue, on_delete=models.CASCADE, limit_choices_to={'type__code': 'status'})
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =  models.DateTimeField(auto_now=True)
    

class VehicleEntries(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    vehicle_number = models.CharField(max_length=100)
    status =  models.CharField(max_length=7, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    vehicle_registered = models.BooleanField(default=True)
    created_by =  models.DateTimeField(auto_now=True)

# class Visitor(models.Model):
#     uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
#     name = models.CharField(max_length=100)
#     flat = models.CharField(max_length=10)
#     entry_time = models.DateTimeField(auto_now_add=True)
#     updated_at =  models.DateTimeField(auto_now=True)

# class Notice(models.Model):
#     uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     date_posted = models.DateTimeField(auto_now_add=True)
#     updated_at =  models.DateTimeField(auto_now=True)
