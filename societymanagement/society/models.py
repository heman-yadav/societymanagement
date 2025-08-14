from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
import uuid

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
        return self.first_name + " " + self.last_name


class Complaint(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(MasterValue, on_delete=models.CASCADE, limit_choices_to={'type__code': 'complaint_category'}, related_name='complaint_type')
    priority = models.ForeignKey(MasterValue, on_delete=models.CASCADE, limit_choices_to={'type__code': 'priority'}, related_name='priority')
    status = models.ForeignKey(MasterValue, on_delete=models.CASCADE, limit_choices_to={'type__code': 'status'})
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} for flat {self.category}"
    

class VehicleEntries(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    vehicle_number = models.CharField(max_length=100)
    status =  models.CharField(max_length=7, blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    vehicle_registered = models.BooleanField(default=True)
    created_by =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle_number} for flat {self.status}"


class VisitorEntries(models.Model):
    flat = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='flat', related_name='flat_num_reqest')
    visitor_name = models.CharField(max_length=100)
    purpose = models.ForeignKey(MasterValue, on_delete=models.CASCADE, limit_choices_to={'type__code': 'visitor_purpose'}, related_name='visitor_purpose')
    status = models.ForeignKey(MasterValue, on_delete=models.CASCADE, limit_choices_to={'type__code': 'status'}, related_name='visitor_req_status')
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gatekeeper_requests')
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='resident_approvals')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.visitor_name} for flat {self.flat}"

# class Notice(models.Model):
#     uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     date_posted = models.DateTimeField(auto_now_add=True)
#     updated_at =  models.DateTimeField(auto_now=True)

# models.py
class Notice(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    image = models.ImageField(upload_to='notices/', blank=True, null=True)
    crated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # ensures latest first by default

    def __str__(self):
        return self.title


class ProfileImage(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    
    image = models.ImageField(upload_to='staff_profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.id


