from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile, Job, Application

class SeekerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'SEEKER'
        if commit:
            user.save()
        return user

class EmployerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'EMPLOYER'
        if commit:
            user.save()
        return user

class SeekerProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['resume', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
        }

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['company_name', 'company_description']
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': 'Enter company name'}),
            'company_description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about your company...'}),
        }

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company_name', 'location', 'salary_range', 'job_type', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Job Title'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'Company Name'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Remote, San Francisco, NY'}),
            'salary_range': forms.TextInput(attrs={'placeholder': 'e.g. $80,000 - $100,000'}),
            'job_type': forms.Select(choices=Job.JOB_TYPES),
            'description': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Provide job description and requirements...'}),
        }

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=Application.STATUS_CHOICES),
        }
