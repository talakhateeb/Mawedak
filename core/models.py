# from django.db import models
# from django.contrib.auth.models import User

# class Department(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()

#     def __str__(self):
#         return self.name

# class Service(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name

# class Appointment(models.Model):
#     STATUS_CHOICES = [
#         ('Pending', 'Pending'),
#         ('In Progress', 'In Progress'),
#         ('Completed', 'Completed'),
#         ('Canceled', 'Canceled'),
#     ]

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     service = models.ForeignKey(Service, on_delete=models.CASCADE)
#     appointment_date = models.DateTimeField()
#     queue_number = models.IntegerField()
#     status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

#     def __str__(self):
#         return f"Appointment {self.id} for {self.user.username}"


from django.db import models
from django.contrib.auth.models import User

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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    queue_number = models.IntegerField(blank=True, null=True)  # Allow null initially
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def save(self, *args, **kwargs):
        if self.queue_number is None:  # Only assign if queue_number is not set
            # Get the highest queue number for the same service
            last_appointment = Appointment.objects.filter(service=self.service).order_by('-queue_number').first()
            if last_appointment:
                self.queue_number = last_appointment.queue_number + 1  # Increment the last queue number
            else:
                self.queue_number = 1  # Start with 1 if no previous appointments exist
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment {self.id} for {self.user.username}"