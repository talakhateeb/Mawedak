from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import RegisterForm, AppointmentForm
from .models import Appointment, Service, Department
from django.contrib.auth.forms import UserCreationForm



def home(request):
    """Render the home page."""
    return render(request, 'core/home.html')


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
    return render(request, 'core/queue.html')


def register(request):
    """User registration view."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "حدث خطأ أثناء التسجيل.")
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def get_departments(request):
    departments = Department.objects.all().values('id', 'name')  # Fetch department id and name
    return JsonResponse(list(departments), safe=False)


# @api_view(['GET'])
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
def create_appointment(request):
    """View to create an appointment."""
    # Fetch all departments and their related services
    departments = Department.objects.all()
    services_by_department = {
        department.id: Service.objects.filter(department=department)
        for department in departments
    }

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Save the appointment for the logged-in user
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(request, 'تم إنشاء الموعد بنجاح!')
            return redirect('appointment_list')  # Redirect to the appointment list
    else:
        form = AppointmentForm()

    return render(
        request,
        'core/appointment.html',
        {
            'form': form,
            'departments': departments,
            'services_by_department': services_by_department,
        },
    )


# @login_required
def appointment_list(request):
    """View to display the logged-in user's appointments."""
    appointments = Appointment.objects.filter(user=request.user).select_related('service')
    return render(request, 'core/appointment_list.html', {'appointments': appointments})


def get_services(request, department_id):
    """
    Fetch services for a specific department.
    """
    print(f"Fetching services for department ID: {department_id}")  # Debug log
    try:
        services = Service.objects.filter(department_id=department_id)
        print(f"Services found: {services}")  # Debug log
        services_data = [
            {"id": service.id, "name": service.name}
            for service in services
        ]
        return JsonResponse(services_data, safe=False)
    except Exception as e:
        print(f"Error fetching services: {e}")  # Debug log
        return JsonResponse({"error": str(e)}, status=500)




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