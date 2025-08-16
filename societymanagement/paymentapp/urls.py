from django.urls import path
from .views import *

urlpatterns = [
    path('pay/', PhonePeDemoView.as_view(), name='phonepe_pay'),
    path('callback/', PhonePeCallbackView.as_view(), name='phonepe_callback'),
    path('payment-transaction-list', PaymentTransactionListView.as_view(), name="payment-transaction-list")
]   