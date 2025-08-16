from django.shortcuts import render
from django.conf import settings
from .models import *
from .forms import *
from django.views import View
from django.views.generic import CreateView, ListView
from django.shortcuts import render, redirect
from django.urls import reverse
from phonepe import PhonePe
from django.db import transaction
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import json

# Create your views here.


class PhonePeDemoView(LoginRequiredMixin, View):
    template_name = 'society/phonepe_demo.html'
    model = PaymentMaster
    form_class = PaymentForm

    def get(self, request):
        context = {'form': self.form_class()}
        return render(request, self.template_name, context)

    @transaction.atomic
    def post(self, request):

        form = PaymentForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        # Extract validated form data
        amount = int(form.cleaned_data["amount"])
        payment_type = form.cleaned_data["type"]

        # Generate order/transaction ID
        transaction_id = str(uuid.uuid4())
        user_id = request.user if request.user.is_authenticated else None

        # Save initial transaction
        txn = PaymentTransaction.objects.create(
            uid = transaction_id,
            user=user_id,
            transaction_id=transaction_id,
            amount=amount,
            type=payment_type,
            status= PaymentTransaction.Status.INITIATED
        )

        # Instantiate PhonePe client
        phonepe = PhonePe(
            merchant_id=settings.APP_CONFIG.get("PHONEPE_MERCHANT_ID"),
            phone_pe_salt=settings.APP_CONFIG.get("PHONEPE_SALT_KEY"),
            phone_pe_host=settings.APP_CONFIG.get("PHONEPE_HOST"),
            redirect_url=request.build_absolute_uri(reverse('phonepe_callback')),
            webhook_url=request.build_absolute_uri(reverse('phonepe_callback')),
            phone_pe_salt_index=settings.PHONEPE_SALT_INDEX
        )
        
        try:
            # Create a demo transaction
            user_id = str(request.user.id) if request.user.is_authenticated else 'anonymous'
            result = phonepe.create_txn(transaction_id, amount=amount, user=str(user_id or "guest"))

            payment_url = result["data"]["instrumentResponse"]["redirectInfo"]["url"]

            print('result: ', result)

            txn.provider_txn_id = result["data"].get("merchantTransactionId")
            txn.merchant_id = result['data'].get('merchantId')
            txn.save()
            return redirect(payment_url)
        except Exception as e:
            txn.status = PaymentTransaction.Status.FAILED
            txn.response_payload = {"error": str(e)}
            txn.save()
            return JsonResponse({"error": "Transaction failed", "details": str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class PhonePeCallbackView(View):
    def post(self, request):
        try:
            data = None

            # Case 1: JSON in raw body
            try:
                data = json.loads(request.body.decode())
                print("Parsed JSON body:", data)
            except Exception:
                pass

            # Case 2: Form-encoded data
            if not data and request.POST:
                data = request.POST.dict()
                print("Parsed Form POST:", data)

            if not data:
                return render(request, "payment_result.html", {
                    "message": "No callback data received",
                    "transaction": None
                })

            merchantId = data.get("merchantId")
            print('merchantId:',merchantId)
            provider_txn_id = data.get("transactionId")
            print("provider_txn_id: ", provider_txn_id)
            txn_status = data.get("code")
            print("txn_status: ", txn_status)

            with transaction.atomic():
                txn = PaymentTransaction.objects.filter(transaction_id=provider_txn_id).first()
                print('txn: ', txn)

                if provider_txn_id:
                    txn.provider_txn_id = provider_txn_id

                if txn_status == "PAYMENT_SUCCESS":
                    txn.status = PaymentTransaction.Status.SUCCESS
                elif txn_status == "PAYMENT_PENDING":
                    txn.status = PaymentTransaction.Status.PENDING
                else:
                    txn.status = PaymentTransaction.Status.FAILED

                txn.response_payload = data
                txn.save()

            return redirect('payment-transaction-list')

        except Exception as e:
            print('error',e.__traceback__.tb_lineno)
            return render(request, "society/payment_result.html", {
                "message": "Callback handling failed",
                "transaction": None,
                "error": str(e),
            })


class PaymentTransactionListView(LoginRequiredMixin, ListView):
    model = PaymentTransaction
    template_name = "society/transaction_list.html"
    paginate_by = 7

    def get_queryset(self):
        qs = super().get_queryset()

        # Admins can see all complaints
        if self.request.user.is_staff or self.request.user.is_superuser:
            return qs
        # Normal users see only their own complaints
        return qs.filter(user=self.request.user)