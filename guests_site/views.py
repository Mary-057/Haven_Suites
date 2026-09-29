from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .forms import guestsForm, GuestBookingForm

# DRF Imports for the API
from rest_framework import viewsets, generics, permissions  # type: ignore[import-not-found]

from .forms import guestsForm
from .models import guests_registration
from .serializers import GuestSerializer, GuestRegistrationSerializer
from django.contrib.auth import login

def guest_signup_view(request):
    # If they are already logged in, send them away
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard')
        return redirect('guest_dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False # Enforce security: new public users are NEVER staff
            user.save()
            login(request, user) # Automatically log them in
            return redirect('guest_dashboard')
    else:
        form = UserCreationForm()
        
    return render(request, 'guest_signup.html', {'form': form})
# --- HTML FRONTEND VIEWS (INTERNAL STAFF DASHBOARD) ---

# 1. Secured Add Staff View (Function-Based)
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='dashboard')
def add_staff_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            messages.success(request, f"Staff account for '{user.username}' created successfully!")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'add_staff.html', {'form': form})


@login_required
def register_guest(request):
    form = guestsForm()
    if request.method == 'POST':
        form = guestsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Guest registered successfully!")
            return redirect('dashboard')
    context = {"form": form}
    return render(request, 'home.html', context)


@login_required
def dashboard_view(request):
    all_guests = guests_registration.objects.all().order_by('-date_recorded')
    context = {'all_guests': all_guests} 
    return render(request, 'dashboard.html', context)


class GuestUpdateView(LoginRequiredMixin, UpdateView):
    model = guests_registration
    form_class = guestsForm
    template_name = "guest_update.html"
    success_url = reverse_lazy('dashboard')


# 2. Secured Delete Guest View (Class-Based)
class GuestDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = guests_registration
    template_name = "guest_delete.html" 
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('dashboard')


class GuestDetailView(LoginRequiredMixin, DetailView):
    model = guests_registration
    template_name = "guest_detail.html"
    context_object_name = 'guest'
    

class GuestCreateView(LoginRequiredMixin, CreateView):
    model = guests_registration
    form_class = guestsForm
    template_name = "guest_create.html"
    success_url = reverse_lazy('dashboard')


# --- REST API VIEWS (PUBLIC GUEST API & DATA ISOLATION) ---

# API Endpoint for Guests to Register Themselves
class APIGuestRegistrationView(generics.CreateAPIView):
    serializer_class = GuestRegistrationSerializer
    permission_classes = [permissions.AllowAny] # Unauthenticated public users can access this

# API Endpoint for Role-Based Data Isolation (The "Security Guard")
class APIGuestViewSet(viewsets.ModelViewSet):
    serializer_class = GuestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # Staff Visibility: Security guard hands the serializer ALL hotel records
        if user.is_staff or user.is_superuser:
            return guests_registration.objects.all().order_by('-date_recorded')
            
        # Guest Visibility (Data Isolation): Security guard hands the serializer ONLY their own record
        return guests_registration.objects.filter(guest_user=user)

    def perform_create(self, serializer):
        # Automatically links the logged-in guest to the booking record they just created
        serializer.save(guest_user=self.request.user)
@login_required
def dashboard_view(request):
    # THE BOUNCER: If the user is NOT staff, redirect them to their isolated guest view
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('guest_dashboard')
        
    # If they ARE staff, load all the records
    all_guests = guests_registration.objects.all().order_by('-date_recorded')
    context = {'all_guests': all_guests} 
    return render(request, 'dashboard.html', context)

@login_required
def guest_dashboard_view(request):
    # If a staff member accidentally navigates here, redirect them to the staff dashboard
    if request.user.is_staff or request.user.is_superuser:
        return redirect('dashboard')
    
    # Try to find the booking linked to this specific logged-in guest
    try:
        booking = guests_registration.objects.get(guest_user=request.user)
    except guests_registration.DoesNotExist:
        booking = None
        
    context = {'booking': booking}
    return render(request, 'guest_dashboard.html', context)

@login_required
def guest_create_booking_view(request):
    # Bounce staff members back to the main dashboard
    if request.user.is_staff or request.user.is_superuser:
        return redirect('dashboard')
        
    # Prevent guests from booking twice (since they only get one active room at a time)
    if guests_registration.objects.filter(guest_user=request.user).exists():
        return redirect('guest_dashboard')

    if request.method == 'POST':
        form = GuestBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.guest_user = request.user # Silently links the booking to their account
            booking.save()
            return redirect('guest_dashboard')
    else:
        form = GuestBookingForm()
        
    return render(request, 'guest_book.html', {'form': form})