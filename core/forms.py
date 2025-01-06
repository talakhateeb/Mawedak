from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import Appointment, Service, Department

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class AppointmentForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        label="اختر الدائرة",
        required=True,
        widget=forms.Select(attrs={'id': 'department-select'})
    )
    service = forms.ModelChoiceField(
        queryset=Service.objects.none(),
        label="اختر الخدمة",
        required=True,
        widget=forms.Select(attrs={'id': 'service-select'})
    )

    class Meta:
        model = Appointment
        fields = ['department', 'service', 'appointment_date']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['service'].queryset = Service.objects.filter(department_id=department_id)
            except (ValueError, TypeError):
                pass
        else:
            self.fields['service'].queryset = Service.objects.none()

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data['appointment_date']
        # Check if the appointment already exists at this date and time
        if Appointment.objects.filter(appointment_date=appointment_date).exists():
            raise forms.ValidationError("الوقت المحدد غير متاح")
        return appointment_date

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'department']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Service Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Service Description'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Service.objects.filter(name=name).exists():
            raise forms.ValidationError("A service with this name already exists.")
        return name

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Department Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Department Description'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Department.objects.filter(name=name).exists():
            raise forms.ValidationError("A department with this name already exists.")
        return 
    
    # forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='الاسم', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'أدخل اسمك'
    }))
    email = forms.EmailField(label='البريد الإلكتروني', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'أدخل بريدك الإلكتروني'
    }))
    message = forms.CharField(label='الرسالة', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'أدخل رسالتك',
        'rows': 5
    }))
