from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import guests_registration
from datetime import date

class HavenSuitesTests(TestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = User.objects.create_user(username='teststaff', password='password123')
        
        # Create a sample guest record
        self.guest = guests_registration.objects.create(
            first_name='John',
            last_name='Doe',
            phone_number='08012345678',
            room_number='101',
            number_of_nights=3,
            check_in_date=date.today(),
            recorded_by=self.user
        )

    def test_guest_model_string(self):
        """Test that the guest model string representation is formatted correctly"""
        self.assertEqual(str(self.guest), "John Doe - Room 101")

    def test_login_required_for_dashboard(self):
        """Test that unauthenticated users are redirected away from the dashboard"""
        response = self.client.get(reverse('dashboard'))
        # Should redirect (302) to login page
        self.assertEqual(response.status_code, 302)

    def test_dashboard_access_when_logged_in(self):
        """Test that authenticated staff can successfully access the dashboard"""
        self.client.login(username='teststaff', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')