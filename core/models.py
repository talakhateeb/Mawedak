from django.db import models
from django.contrib.auth.models import User


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'رسالة من {self.name} ({self.email})'
        
class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the logged-in user
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)  # Assuming Service model exists
    appointment_date = models.DateTimeField() 
    appointment_time = models.TimeField() 
    queue_number = models.IntegerField(blank=True, null=True)  # Optional queue number
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    phone = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    notes = models.TextField(blank=True, null=True) 

    def save(self, *args, **kwargs):
        if self.queue_number is None:
            last_appointment = Appointment.objects.filter(service=self.service).order_by('-queue_number').first()
            if last_appointment:
                self.queue_number = last_appointment.queue_number + 1
            else:
                self.queue_number = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment {self.id} for {self.user.username}"

