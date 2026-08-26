from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Job, Application

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name']
    search_fields = ['user__username', 'company_name']

class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'location', 'job_type', 'created_at']
    list_filter = ['job_type', 'created_at']
    search_fields = ['title', 'company_name', 'location']

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['job', 'applicant', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['job__title', 'applicant__username']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)
