from django.contrib import messages  # <-- Make sure to import messages at the top
from django.shortcuts import render, redirect  # type: ignore[reportMissingImports]
from django.contrib.auth.decorators import login_required  # type: ignore[reportMissingImports]
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView  # type: ignore[reportMissingImports]
from django.urls import reverse_lazy  # type: ignore[reportMissingImports]
from .forms import guestsForm
from .models import guests_registration
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
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
def add_staff_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  # Give them staff permissions
            user.save()
            messages.success(request, f"Staff account for '{user.username}' created successfully!")
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'add_staff.html', {'form': form})

def register_guest(request):
    form = guestsForm()
    if request.method == 'POST':
        form = guestsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Guest registered successfully!")  # <-- Success popup message
            return redirect('dashboard')  # <-- Redirects to dashboard after successful registration
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


class GuestDeleteView(DeleteView):
    model = guests_registration
    template_name = "guest_delete.html" 
    success_url = reverse_lazy('dashboard')


class GuestDetailView(DetailView):
    model = guests_registration
    template_name = "guest_detail.html"
    context_object_name = 'guest'
    

class GuestCreateView(CreateView):
    model = guests_registration
    form_class = guestsForm
    template_name = "guest_create.html"
    success_url = reverse_lazy('dashboard')