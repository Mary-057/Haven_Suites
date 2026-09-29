from rest_framework import serializers  # type: ignore[import-not-found]
from django.contrib.auth.models import User
from .models import guests_registration

# 1. Serializer to translate your updated guest model into JSON
class GuestSerializer(serializers.ModelSerializer):
    # This ensures the room_type displays the readable name (e.g., "Deluxe Room" instead of "deluxe")
    room_type_display = serializers.CharField(source='get_room_type_display', read_only=True)
    
    class Meta:
        model = guests_registration
        fields = '__all__'

# 2. Serializer for public guests to create a login account
class GuestRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Creates a secure user account, ensuring they are NOT marked as staff
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            is_staff=False 
        )
        return user