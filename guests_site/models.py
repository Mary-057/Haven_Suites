from django.db import models
from django.contrib.auth.models import User

class guests_registration(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=False, null=True) # Added phone number
    email = models.EmailField(blank=True, null=True)  # Optional email
    room_number = models.CharField(max_length=10)
    number_of_nights = models.PositiveIntegerField()
    check_in_date = models.DateField()
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Room {self.room_number}"