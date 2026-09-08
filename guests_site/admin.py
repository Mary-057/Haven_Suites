from django.contrib import admin  # type: ignore[reportMissingImports]
from .models import guests_registration
# Register your models here
admin.site.register(guests_registration)