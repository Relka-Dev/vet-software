from django.contrib import admin
from .models import Role, Employee, DisponibilityRange

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['person', 'first_engagement_date', 'role']
    list_filter = ['role']

@admin.register(DisponibilityRange)
class DisponibilityRangeAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date']
