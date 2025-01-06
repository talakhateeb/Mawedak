from django.urls import path
from . import views
from .views import get_services






#     path('appointments/', views.appointment_list, name='appointment_list'),  # List user appointments
#     path('create-appointment/', views.create_appointment, name='appointment'),  # Create appointment
#     path('api/services/', v   ),  # API for dynamic service loading
# ]

urlpatterns = [
    path('', views.home, name='home'),  # الصفحة الرئيسية
    path('register/', views.register, name='register'),  # تسجيل المستخدم
    path('accounts/login/', views.login_view, name='login'),  # تسجيل الدخول
    path('accounts/logout/', views.LogoutView, name='logout'),  # تسجيل الخروج
    path('appointment/', views.create_appointment, name='appointment'),  # إنشاء موعد
    path('appointments/', views.appointment_list, name='appointment_list'),  # قائمة المواعيد
    path('queue/', views.queue, name='queue'),  # تتبع الصف
    path('contact/', views.contact, name='contact'),  # صفحة "اتصل بنا"
    path('about_us/', views.about_us, name='about_us'),  # صفحة "حول "

    # API Endpoints
    path('api/departments/', views.get_departments, name='get_departments'),
    path('api/services/<int:department_id>/', views.get_services, name='get_services'),
    path('api/appointments/', views.appointments_view, name='appointments'),
    path('api/queue-status/', views.get_queue_status, name='get_queue_status'),
    path("api/reserved-times/<int:service_id>/<str:date>/", views.reserved_times, name="reserved_times"),
    path('api/user-appointments/', views.user_appointments_api, name='user_appointments_api'),
    path('api/current-queue/', views.current_queue_api, name='current_queue_api'),
]
