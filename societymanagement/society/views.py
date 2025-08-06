from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .forms import *
from .utils import send_email


# Create your views here.
class RegistrationView(CreateView):
    model = User
    form_class = CustomUserForm
    template_name = "society/registration.html"
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        mobile_number = form.cleaned_data['mobile']
        car_number = form.cleaned_data['car_number']
        car_number = str(car_number).strip().upper()
        bike_number = form.cleaned_data['bike_number']
        bike_number = str(bike_number).strip().upper()
        # ex: +919936409592 I am just storing withot country code number.
        user.mobile = str(mobile_number.national_number)
        user.set_password(form.cleaned_data['password1'])
        user.bike_number = bike_number
        user.car_number = car_number
        user.save()
        messages.success(self.request, "Registration successful!")
        send_email(
                recipient_email=email.strip(),
                subject="Complaint registered successfully:",
                message_body=f"Dear {first_name} {last_name}, We have received your complaint. Our concern persorn will contact you soon."
            )
        return super().form_valid(form)
    
class UserProfileUpdateView(UpdateView):
    model = CustomUser
    slug_field = 'uid'
    form_class = UserProfileUpdateForm
    template_name = "society/user_profile_update.html"
    success_url = reverse_lazy('dashboard')

    
    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, uid=self.kwargs['uid'])


class LoginView(View):
    template_name = 'society/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data['mobile']
            password = form.cleaned_data['password']
            user = authenticate(request, mobile=mobile.national_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # or wherever you want
            else:
                messages.error(request, "Invalid mobile number or password")
                return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class DashboardView(LoginRequiredMixin,TemplateView):
    model = Complaint
    template_name = "society/dashboard.html"


class ComplaintCreateView(LoginRequiredMixin, CreateView):
    form_class = ComplaintModelForm
    template_name = 'society/complaint.html'
    success_url = reverse_lazy('complaints')

    def form_valid(self, form):
        not_started_object = MasterValue.objects.filter(value='Not Started').first()
        form_data = form.save(commit=False)
        user = self.request.user
        form_data.user = user
        form_data.status = not_started_object
        form_data.save()
        return super().form_valid(form)


class ComplaintListView(LoginRequiredMixin, ListView):
    model = Complaint
    paginate_by = 7
    template_name = 'society/complaints.html'


class VehicleEntriesCreateView(LoginRequiredMixin, CreateView):
    models = VehicleEntries
    template_name = 'society/vehicle_entries.html'
    form_class = VehicleEntreisModelForm
    success_url = reverse_lazy('vehicle-entry')

    def form_valid(self, form):
        form_data = form.save(commit=False)

        # Get button clicked: 'entry' or 'exit'
        button_value = self.request.POST.get('action')
        form_data.status = button_value  # Save the action as status

        # Get the vehicle number from the form
        vehicle_number = form.cleaned_data.get('vehicle_number')
        vehicle_number = str(vehicle_number).strip().upper()
        form_data.vehicle_number = vehicle_number
        # Check if this vehicle is registered in your user model
        vehicle_number_check = CustomUser.objects.filter(Q(car_number=vehicle_number) | Q(bike_number=vehicle_number)).first()
        print('vehicle_number_check:', vehicle_number_check)
        if vehicle_number_check:
            form_data.vehicle_registered = True
        else:
            form_data.vehicle_registered = False
        form_data.save()
        return super().form_valid(form)


class VehicleEntriesListView(LoginRequiredMixin, ListView):
    model = VehicleEntries
    paginate_by = 7
    template_name = 'society/cars_entry_list.html'



# class ProfileView(TemplateView):
#     template_name = 'society/profile.html'