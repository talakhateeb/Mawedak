from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import Appointment, Service, Department

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

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
        return name