
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from .forms import RegisterForm, AppointmentForm, ContactForm
from .models import Appointment, Service, Department, ContactMessage
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, time, timedelta
from django.utils import timezone



def about_us(request):
    return render(request, 'core/about_us.html')

def home(request):
    """Render the home page."""
    return render(request, 'core/home.html')

def appointment_list(request):
    """View to list all appointments for the logged-in user."""
    appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'core/appointment_list.html', {'appointments': appointments})



def appointments_view(request):
    """View to fetch appointments for the logged-in user."""
    if request.user.is_authenticated:
        appointments = Appointment.objects.filter(user=request.user)
        appointment_data = [
            {
                'service': appointment.service.name,
                'date': appointment.date,
                'time': appointment.time,
            }
            for appointment in appointments
        ]
        return JsonResponse(appointment_data, safe=False)
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

def queue(request):
    """Render the queue tracking page."""
    if request.is_ajax():
        user_appointments = Appointment.objects.filter(user=request.user).values(
            'id', 'service__name', 'department__name', 'appointment_date', 'status'
        )
        return JsonResponse(list(user_appointments), safe=False)
    else:
        return render(request, 'queue.html')

def reserved_times(request, service_id, date):
    if request.method == "GET":
        start_time = time(8, 0)  
        end_time = time(14, 0)  
        intervals = []

        current_time = datetime.combine(datetime.today(), start_time)
        end_datetime = datetime.combine(datetime.today(), end_time)

        while current_time.time() <= end_datetime.time():
            intervals.append(current_time.strftime("%H:%M"))
            current_time += timedelta(minutes=30)

        reserved_appointments = Appointment.objects.filter(
            service_id=service_id,
            appointment_date__date=date,
        ).values_list("appointment_date", flat=True)

        reserved_times = [time.strftime("%H:%M") for time in reserved_appointments]

        available_times = [slot for slot in intervals if slot not in reserved_times]

        return JsonResponse({"available_times": available_times}, safe=False)

    return JsonResponse({"error": "Invalid request method"}, status=400)



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = RegisterForm()

    return render(request, 'core/register.html', {'form': form})


def get_departments(request):
    departments = Department.objects.all().values('id', 'name')  # Fetch department id and name
    return JsonResponse(list(departments),safe=False)

def get_services(request, department_id):
    try:
        department = Department.objects.get(id=department_id)
        services = Service.objects.filter(department=department)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)
    except Department.DoesNotExist:
        return Response({"detail": "Department not found."}, status=status.HTTP_404_NOT_FOUND)

def login_view(request):
    """User login view."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'تم تسجيل الدخول بنجاح!')
            return redirect('home') 
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة.')
    return render(request, 'core/login.html')

def LogoutView(request):
    """Log out the user and redirect to home page."""
    logout(request)
    return redirect('home')

# @login_required
# def create_appointment(request):
#     """View to create an appointment."""
#     departments = Department.objects.all()
#     user = request.user
#     services_by_department = {
#         department.id: Service.objects.filter(department=department)
#         for department in departments
#     }

#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
        
#             appointment = form.save(commit=False)
#             appointment.user = request.user
#             appointment.save()
#             messages.success(request, 'تم إنشاء الموعد بنجاح!')
#             return redirect('/appointments')  
#         else:
            
#             return render(request, 'core/appointment.html', {
#                 'form': form,
#                 'departments': departments,
#                 'services_by_department': services_by_department,
#             })
#     else:
#         form = AppointmentForm()

#     return render(request,'core/appointment.html',{'form': form,'departments': departments,'services_by_department': services_by_department,},)



#######################################################################################
#######################################################################################
#######################################################################################

@login_required
def create_appointment(request):
    if request.method == 'POST':
        user = request.user
        full_name = f"{user.first_name} {user.last_name}"
        email = user.email
        service_id = request.POST['service']
        appointment_date = request.POST['date']
        appointment_time = request.POST['time']
        department = request.POST['department']
        phone = request.POST.get('phone', '')
        notes = request.POST.get('notes', '')

        # Create appointment
        Appointment.objects.create(
            user=user,
            service_id=service_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            department_id=department,
            phone=phone,
            notes=notes,
        )
        return redirect('/queue')
    return render(request, 'core/appointment.html')


# @login_required 
# def book_appointment(request):
#     # Get logged-in user's name and email
#     user = request.user
#     full_name = f"{user.first_name} {user.last_name}"  # Combine first and last names
#     email = user.email

#     # Pass the information to the template
#     return render(request, 'appointment/book_appointment.html', {
#         'full_name': full_name,
#         'email': email,
#     })

# @login_required
# def save_appointment(request):
#     if request.method == 'POST':


#         # Create the appointment
#         Appointment.objects.create(
#             user=user,
#             full_name=full_name,
#             email=email,
#             phone=request.POST['phone'],
#             service_id=request.POST['service'],
#             appointment_date=request.POST['date'],
#             notes=request.POST.get('notes', ''),
#         )
#         return redirect('appointment_success')
#######################################################################################
#######################################################################################
#######################################################################################



@login_required
def appointment_list(request):
    """View to display the logged-in user's appointments."""
    appointments = Appointment.objects.filter(user=request.user).select_related('service')
    return render(request, 'core/appointment_list.html', {'appointments': appointments})


def get_services(request, department_id):
    """
    Fetch services for a specific department.
    """
    print(f"Fetching services for department ID: {department_id}")  
    try:
        services = Service.objects.filter(department_id=department_id)
        print(f"Services found: {services}")  
        services_data = [
            {"id": service.id, "name": service.name}
            for service in services
        ]
        return JsonResponse(services_data, safe=False)
    except Exception as e:
        print(f"Error fetching services: {e}") 
        return JsonResponse({"error": str(e)}, status=500)



@login_required
def queue(request):
    """View to track queue status."""
    queue_details = None
    error = None

    if request.method == "POST":
        queue_number = request.POST.get('queue_number')
        try:
            # Fetch the appointment by queue number
            queue_details = Appointment.objects.get(queue_number=queue_number)
        except Appointment.DoesNotExist:
            error = "رقم الحجز غير موجود. يرجى التحقق وإعادة المحاولة."

    return render(request, 'core/queue.html', {'queue_details': queue_details, 'error': error})

def get_queue_status(request):
    """API endpoint to fetch queue status by queue number."""
    queue_number = request.GET.get('queue_number')
    try:
        # Fetch the appointment details
        appointment = Appointment.objects.get(queue_number=queue_number)
        data = {
            'user': appointment.user.username,
            'service': appointment.service.name,
            'appointment_date': appointment.appointment_date.strftime('%Y-%m-%d %H:%M'),
            'queue_number': appointment.queue_number,
            'status': appointment.get_status_display(),
        }
        return JsonResponse({'success': True, 'data': data})
    except Appointment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'رقم الحجز غير موجود.'})

def contact(request):
    """View for the contact page."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # حفظ الرسالة في قاعدة البيانات
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                message=form.cleaned_data['message']
            )

            messages.success(request, 'تم إرسال رسالتك بنجاح! سنقوم بالرد عليك قريبًا.')
            return redirect('contact')
        else:
            messages.error(request, 'هناك خطأ في البيانات المدخلة. يرجى المحاولة مرة أخرى.')
    else:
        form = ContactForm()

    context = {
        'form': form
    }
    return render(request, 'core/contact.html', context)

@login_required
def user_appointments_api(request):
    appointments = (
        Appointment.objects.filter(user=request.user)
        .select_related('service', 'department')
        .values(
            'id',
            'service__name',
            'department__name',
            'appointment_date',
            'appointment_time',
            'status',
            'queue_number',
        )
    )

    return JsonResponse(list(appointments), safe=False)

def current_queue_api(request):
    current_queue = Appointment.objects.filter(status='in_progress').order_by('queue_number').first()

    if current_queue:
        data = {'message': f"الدور الحالي في الطابور: {current_queue.queue_number}"}
    else:
        data = {'message': 'لا يوجد طابور نشط حالياً.'}
    
    return JsonResponse(data)

