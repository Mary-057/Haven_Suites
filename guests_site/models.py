from django.db import models
from django.contrib.auth.models import User

class guests_registration(models.Model):
    ROOM_TYPES = [
        ('standard', 'Standard Room'),
        ('deluxe', 'Deluxe Room'),
        ('suite', 'Executive Suite'),
    ]

    guest_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='guest_booking', null=True, blank=True)
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=False, null=True) 
    email = models.EmailField(blank=True, null=True) 
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='standard')
    room_number = models.CharField(max_length=10, blank=True, null=True) 
    number_of_nights = models.PositiveIntegerField()
    check_in_date = models.DateField()
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='staff_recorded_bookings', null=True, blank=True)
    date_recorded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        assigned_room = self.room_number if self.room_number else "Pending Assignment"
        return f"{self.first_name} {self.last_name} - {self.get_room_type_display()} ({assigned_room})"