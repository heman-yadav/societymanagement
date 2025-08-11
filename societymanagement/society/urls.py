from django.urls import path
from .views import *



urlpatterns = [
    path('registration/', RegistrationView.as_view(), name="registration"),
    path('user-update-profile/<uuid:uid>/', UserProfileUpdateView.as_view(), name='user-update-profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('complaints/', ComplaintCreateView.as_view(), name='complaints'),
    path('complaints-list/', ComplaintListView.as_view(), name='complaints-list'),
    path('vehicle-entry/', VehicleEntriesCreateView.as_view(), name='vehicle-entry'),
    path('vehicle-entries-list/', VehicleEntriesListView.as_view(), name='vehicle-entries-list'),
    path('create-visitor-request/', VisitorRequestCreateView.as_view(), name="create-visitor-request"),
    path('visitor-list/', VisitorRequestListView.as_view(), name='visitor-list'),
    path('visitor/<int:pk>/approve-reject/', ApproveRejectVitisorUpdateView.as_view(), name="visitor-approve-reject")
    # path('profile/', views.ProfileView.as_view(), name='profile'),
]