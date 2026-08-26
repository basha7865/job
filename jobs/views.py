from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import User, Profile, Job, Application
from .forms import (
    SeekerRegistrationForm,
    EmployerRegistrationForm,
    SeekerProfileForm,
    EmployerProfileForm,
    JobForm,
    ApplicationStatusForm
)

def register_seeker(request):
    if request.user.is_authenticated:
        return redirect('job_list')
    if request.method == 'POST':
        form = SeekerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to the Job Portal.")
            return redirect('job_list')
    else:
        form = SeekerRegistrationForm()
    return render(request, 'jobs/register.html', {'form': form, 'role_name': 'Job Seeker'})

def register_employer(request):
    if request.user.is_authenticated:
        return redirect('job_list')
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to the Job Portal.")
            return redirect('job_list')
    else:
        form = EmployerRegistrationForm()
    return render(request, 'jobs/register.html', {'form': form, 'role_name': 'Employer'})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('job_list')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('job_list')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'jobs/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.user.role == 'SEEKER':
        if request.method == 'POST':
            form = SeekerProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('profile')
        else:
            form = SeekerProfileForm(instance=profile)
    else: # EMPLOYER
        if request.method == 'POST':
            form = EmployerProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('profile')
        else:
            form = EmployerProfileForm(instance=profile)
    
    return render(request, 'jobs/profile.html', {'form': form})

def job_list(request):
    query = request.GET.get('q', '')
    location = request.GET.get('loc', '')
    job_type = request.GET.get('type', '')

    jobs = Job.objects.all().order_by('-created_at')

    if query:
        jobs = jobs.filter(title__icontains=query) | jobs.filter(description__icontains=query) | jobs.filter(company_name__icontains=query)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    context = {
        'jobs': jobs,
        'query': query,
        'location': location,
        'job_type': job_type,
    }
    return render(request, 'jobs/job_list.html', context)

def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    already_applied = False
    if request.user.is_authenticated and request.user.role == 'SEEKER':
        already_applied = Application.objects.filter(job=job, applicant=request.user).exists()
    
    context = {
        'job': job,
        'already_applied': already_applied,
    }
    return render(request, 'jobs/job_detail.html', context)

@login_required
def create_job(request):
    if request.user.role != 'EMPLOYER':
        messages.error(request, "Access denied. Only employers can post jobs.")
        return redirect('job_list')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, "Job posting created successfully!")
            return redirect('job_detail', job_id=job.id)
    else:
        form = JobForm()
    return render(request, 'jobs/create_job.html', {'form': form, 'action_name': 'Post'})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if job.employer != request.user:
        messages.error(request, "You do not have permission to edit this job.")
        return redirect('job_list')
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job posting updated successfully!")
            return redirect('job_detail', job_id=job.id)
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/create_job.html', {'form': form, 'action_name': 'Edit'})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if job.employer != request.user:
        messages.error(request, "You do not have permission to delete this job.")
        return redirect('job_list')
    
    if request.method == 'POST':
        job.delete()
        messages.success(request, "Job posting deleted successfully.")
        return redirect('employer_dashboard')
    
    return render(request, 'jobs/delete_job.html', {'job': job})

@login_required
def apply_job(request, job_id):
    if request.user.role != 'SEEKER':
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect('job_detail', job_id=job_id)
    
    job = get_object_or_404(Job, pk=job_id)
    
    try:
        Application.objects.create(job=job, applicant=request.user)
        messages.success(request, f"Successfully applied for {job.title}!")
    except IntegrityError:
        messages.warning(request, "You have already applied for this job.")
        
    return redirect('seeker_dashboard')

@login_required
def employer_dashboard(request):
    if request.user.role != 'EMPLOYER':
        messages.error(request, "Access denied. Only employers can access the employer dashboard.")
        return redirect('job_list')
    
    jobs = Job.objects.filter(employer=request.user).order_by('-created_at')
    # Fetch all applications for jobs posted by this employer
    applications = Application.objects.filter(job__employer=request.user).order_by('-applied_at')
    
    context = {
        'jobs': jobs,
        'applications': applications,
    }
    return render(request, 'jobs/employer_dashboard.html', context)

@login_required
def seeker_dashboard(request):
    if request.user.role != 'SEEKER':
        messages.error(request, "Access denied. Only job seekers can access the seeker dashboard.")
        return redirect('job_list')
    
    applications = Application.objects.filter(applicant=request.user).order_by('-applied_at')
    
    context = {
        'applications': applications,
    }
    return render(request, 'jobs/seeker_dashboard.html', context)

@login_required
def update_application_status(request, app_id):
    application = get_object_or_404(Application, pk=app_id)
    if application.job.employer != request.user:
        messages.error(request, "You do not have permission to update this application.")
        return redirect('employer_dashboard')
    
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated status of {application.applicant.username}'s application to {application.status}.")
    return redirect('employer_dashboard')
