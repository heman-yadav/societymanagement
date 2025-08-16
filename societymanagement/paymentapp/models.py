from django.db import models
from django.conf import settings
import uuid

# Create your models here.
class PaymentMaster(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    type = models.CharField(max_length=100, blank=True, null=True)
    amount = models.PositiveIntegerField()
    is_visible = models.BooleanField(default=False)
    remark = models.CharField(max_length=200, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_author')
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type} {self.amount}"



class PaymentTransaction(models.Model):
    class Status(models.TextChoices):
        INITIATED = "INITIATED", "Initiated"
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"
    uid = models.UUIDField(unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)  # from PhonePe
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    gateway = models.CharField(max_length=50, default="PHONEPE")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INITIATED)
    # PhonePe’s transaction ID
    provider_txn_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    merchant_id =  models.CharField(max_length=100, null=True, blank=True)
    provider_reference_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    merchant_transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    raw_response = models.JSONField(blank=True, null=True)  # store PhonePe callback JSON
    remark = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} | {self.gateway} | {self.amount} {self.currency} | {self.status}"
