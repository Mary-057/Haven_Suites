from django import forms  # type: ignore[reportMissingModuleSource]
from .models import guests_registration

class guestsForm(forms.ModelForm):
    class Meta:
        model = guests_registration
        fields = '__all__'
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}, format='%d/%m/%Y'),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}, format='%d/%m/%Y')
        }



class GuestBookingForm(forms.ModelForm):
    class Meta:
        model = guests_registration
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'room_type', 'number_of_nights', 'check_in_date']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
        }