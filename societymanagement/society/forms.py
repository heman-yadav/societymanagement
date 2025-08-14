# society/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from phonenumber_field.formfields import PhoneNumberField, to_python
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(forms.Form):
    mobile = PhoneNumberField(
        label='Mobile Number',
        region='IN',
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'value': "8299001059",
            'placeholder': 'Enter your mobile number'
        })
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
            'value': "Ganesh@1212",
            "autocomplete": "current-password"
            }),
    )


class CustomUserForm(UserCreationForm):

    mobile = PhoneNumberField(region='IN')
    # tenant_mobile = PhoneNumberField(region='IN')

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', # From AbstractUser
            'owner_type', 'mobile',
            'flat', 'bike_number', 'car_number',
            'id_type', 'id_number',
             'password1', 'password2'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'autofocus': True,}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True,}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'xyz@mail.com'}),
            'owner_type': forms.Select(attrs={'class': 'form-control', 'required': True,}),
            'id_type': forms.Select(attrs={'class': 'form-control', 'required': True,}),
            'flat': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': '71B'}),
            # 'mobile': forms.NumberInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter mobile number without country code'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control', 'required': True,}),
            'car_number': forms.TextInput(attrs={'class': 'form-control text-uppercase', 'placeholder': 'UP14AB0000'}),
            'bike_number': forms.TextInput(attrs={'class': 'form-control text-uppercase', 'placeholder': 'UP14AB0000'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'required': True,}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'required': True,}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in ['id_number', 'car_number', 'bike_number', 'flat']:
                field.widget.attrs['class'] = 'form-control text-uppercase'
            else:
                field.widget.attrs['class'] = 'form-control'
                
    def clean(self):
        cleaned_data = super().clean()
        for field_name, value in cleaned_data.items():
            if isinstance(value, str):
                cleaned_data[field_name] = ' '.join(value.strip().split())
        return cleaned_data

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     first_name = self.cleaned_data.get('first_name')
    #     first_name = self.cleaned_data.get('last_name')
    #     if commit:
    #         user.save()
    #     return user

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', # From AbstractUser
            'owner_type', 'mobile',
            'flat', 'bike_number', 'car_number',
            'id_type', 'id_number',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True,}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True,}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'required': True,}),
            'owner_type': forms.Select(attrs={'class': 'form-control', 'required': True,}),
            'flat': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': '71B'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter mobile number without country code'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control', 'required': True,}),
            'id_type': forms.Select(attrs={'class': 'form-control', 'required': True,}),
            'car_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UP14AB0000'}),
            'bike_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UP14AB0000'}),
        }


class ComplaintModelForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['category', 'priority', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4,'placeholder': 'Enter your complete desciption here'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }


class ComplaintUpdateModelForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status' ,'category', 'priority', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        allowed_statuses = ['Not Started', 'In Process', 'Completed']
        self.fields['status'].queryset = self.fields['status'].queryset.filter(value__in=allowed_statuses)



class VehicleEntreisModelForm(forms.ModelForm):
    class Meta:
        model = VehicleEntries
        fields = ['vehicle_number']

        widgets = {
            'vehicle_number': forms.TextInput(attrs={'class': 'form-control text-uppercase', 'required': True, 'placeholder': 'UP14AB0000'}),
        }


class CreateVisitorReqeustForm(forms.ModelForm):
    class Meta:
        model = VisitorEntries
        fields = ['flat', 'visitor_name', 'purpose']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # showing flat number instead of username name
        self.fields['flat'].queryset = CustomUser.objects.filter(is_active=True).order_by('flat')
        self.fields['flat'].label_from_instance = lambda obj: obj.flat
        self.fields['flat'].widget.attrs['class'] = 'form-control'
        self.fields['visitor_name'].widget.attrs['class'] = 'form-control'
        self.fields['purpose'].widget.attrs['class'] = 'form-control'


class PublishNoticeInfoForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'message', 'image']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter Title'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Enter you message', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }