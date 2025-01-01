from django.urls import path
from . import views
from .views import get_services


urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),  # User registration
    # path('login/', views.login_view, name='login'),  # User login
path('queue/', views.queue, name='queue'),
path('api/queue-status/', views.get_queue_status, name='get_queue_status'),
    path('api/departments/', views.get_departments, name='get_departments'),  # New endpoint
    path('api/services/<int:department_id>/', views.get_services, name='get_services'),  # Correctly captures department_id
    path('api/appointments/', views.appointments_view, name='appointments'),

    path('accounts/login/', views.login_view, name='login'),
        path('accounts/logout/', views.LogoutView, name='logout'),


    path('appointments/', views.appointment_list, name='appointment_list'),  # List user appointments
    path('create-appointment/', views.create_appointment, name='appointment'),  # Create appointment
    path('api/services/', views.get_services, name='get_services'),  # API for dynamic service loading
]
