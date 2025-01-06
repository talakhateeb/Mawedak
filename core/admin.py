from django.contrib import admin
from .models import Department, Service, Appointment

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)  # Allows searching by department name

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    list_filter = ('department',)  # Filter services by department
    search_fields = ('name',)  # Allows searching by service name

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'appointment_date', 'queue_number', 'status')
    list_filter = ('status', 'service', 'appointment_date')  # Filter appointments by status, service, and date
    search_fields = ('user__username', 'service__name')  # Allows searching by username and service name
    ordering = ('appointment_date',)  
