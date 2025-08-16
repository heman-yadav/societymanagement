from django import forms
from .models import *

class PaymentForm(forms.ModelForm):

    type = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Payment Type"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        payment_data = PaymentMaster.objects.values('type', 'amount', 'remark').distinct()
        
        # Create a dictionary to hold type-amount mappings for JavaScript
        type_amount_map = {}
        
        type_choices = [('', 'Select Type')]
        for item in payment_data:
            type_value = item['type']
            amount_value = item['amount']
            
            # Populate choices for the dropdown
            type_choices.append((type_value, type_value))
            
            # Store the mapping for JavaScript
            type_amount_map[type_value] = str(amount_value) # Convert to string for data attribute

        # Assign the choices to the form field
        self.fields['type'].choices = type_choices

        # Make the amount field a plain TextInput and make it read-only
        self.fields['amount'] = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            label="Amount (₹)"
        )
        
        # Pass the mapping to the template via a hidden field or a data attribute
        # A hidden field is a simple way to get it to the template
        self.fields['type_amount_map'] = forms.CharField(
            widget=forms.HiddenInput(),
            initial=type_amount_map
        )

    class Meta:
        model = PaymentMaster
        fields = ['type', 'amount', 'remark']