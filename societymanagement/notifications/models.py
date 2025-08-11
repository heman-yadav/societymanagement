from django.db import models
from django.conf import settings
import uuid
from .models import MasterValue

# Create your models here.
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('visitor', 'Visitor Request'),
        ('complaint', 'New Complaint'),
        ('general', 'General'),
    ]
    uid =  models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    type = models.ForeignKey(MasterValue, on_delete=models.CASCADE, limit_choices_to={'type__code': 'status'})
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    
    # Optional relation to any object (use one of them as needed)
    related_object_id = models.PositiveIntegerField(blank=True, null=True)
    related_model = models.CharField(max_length=100, blank=True)  # e.g., 'Complaint', 'VisitorRequest'
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_notifications', on_delete=models.SET_NULL,null=True, blank=True)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='recipient_notifications', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type.title()} Notification to {self.recipient.username}"
