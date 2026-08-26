from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    ROLE_CHOICES = (
        ('SEEKER', 'Job Seeker'),
        ('EMPLOYER', 'Employer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='SEEKER')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # Seeker fields
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    bio = models.TextField(blank=True)
    # Employer fields
    company_name = models.CharField(max_length=200, blank=True)
    company_description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Job(models.Model):
    JOB_TYPES = (
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
        ('Remote', 'Remote'),
    )
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='Full-Time')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('Accepted', 'Accepted'),
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['job', 'applicant'], name='unique_application')
        ]

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"
