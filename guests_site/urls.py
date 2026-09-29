from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

from . import views
from .views import (
    register_guest, dashboard_view, GuestCreateView, 
    GuestUpdateView, GuestDeleteView, GuestDetailView,
    APIGuestViewSet, APIGuestRegistrationView
)

# 1. Initialize the DRF Router
router = DefaultRouter()
# This automatically creates routes like /api/guests/ (GET/POST) and /api/guests/<id>/ (GET/PUT/DELETE)
router.register(r'guests', APIGuestViewSet, basename='api-guest')

urlpatterns = [
    # --- HTML FRONTEND URLS (STAFF DASHBOARD) ---
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('register/', register_guest, name='register'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('guest-dashboard/', views.guest_dashboard_view, name='guest_dashboard'),
    path('guest-book/', views.guest_create_booking_view, name='guest_book'),
    path('guest/create/', GuestCreateView.as_view(), name='guest_create'),
    path('guest/view/<int:pk>/', GuestDetailView.as_view(), name='guest_detail'),
    path('guest/update/<int:pk>/', GuestUpdateView.as_view(), name='guest_update'),
    path('guest/delete/<int:pk>/', GuestDeleteView.as_view(), name='guest_delete'),
    path('signup/', views.guest_signup_view, name='guest_signup'),
    path('staff/add/', views.add_staff_view, name='add_staff'),
   
    # --- REST API URLS (GUEST-FACING) ---
    path('api/register/', APIGuestRegistrationView.as_view(), name='api-register'),
    path('api/', include(router.urls)),
]