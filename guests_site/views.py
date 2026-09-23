from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .forms import guestsForm
from .models import guests_registration


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


class GuestUpdateView(UpdateView):
    model = guests_registration
    form_class = guestsForm
    template_name = "guest_update.html"
    success_url = reverse_lazy('dashboard')


# 2. Secured Delete Guest View (Class-Based)
class GuestDeleteView(UserPassesTestMixin, DeleteView):
    model = guests_registration
    template_name = "guest_delete.html" 
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('dashboard')


class GuestDetailView(DetailView):
    model = guests_registration
    template_name = "guest_detail.html"
    context_object_name = 'guest'
    

class GuestCreateView(CreateView):
    model = guests_registration
    form_class = guestsForm
    template_name = "guest_create.html"
    success_url = reverse_lazy('dashboard')