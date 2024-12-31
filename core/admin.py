from django.contrib import admin
from .models import Department, Service, Appointment

# Register your models here.

admin.site.register(Department)
admin.site.register(Service)
admin.site.register(Appointment)
