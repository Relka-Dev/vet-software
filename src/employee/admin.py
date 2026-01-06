from django.contrib import admin
from .models import (
    AvailabilityEmployee,
    AvailabilityException,
    OpenException,
    OpenHours,
    Role,
    Employee,
)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['person', 'first_engagement_date', 'role']
    list_filter = ['role']


@admin.register(OpenHours)
class OpenHoursAdmin(admin.ModelAdmin):
    list_display = ['day_of_week', 'start_time', 'end_time', 'start_date', 'end_date']
    list_filter = ['day_of_week']


@admin.register(OpenException)
class OpenExceptionAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date', 'is_open']
    list_filter = ['is_open']


@admin.register(AvailabilityEmployee)
class AvailabilityEmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'employee',
        'day_of_week',
        'start_time',
        'end_time',
        'start_date',
        'end_date',
    ]
    list_filter = ['employee', 'day_of_week']


@admin.register(AvailabilityException)
class AvailabilityExceptionAdmin(admin.ModelAdmin):
    list_display = ['employee', 'start_date', 'end_date', 'is_available']
    list_filter = ['employee', 'is_available']
