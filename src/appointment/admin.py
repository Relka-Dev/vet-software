from django.contrib import admin
from .models import (
    RoomType,
    Room,
    EmergencyType,
    Procedure,
    Equipment,
    Appointment,
)


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_type']


@admin.register(EmergencyType)
class EmergencyTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'animal',
        'room',
        'employee',
        'emergency_type',
        'start_date',
        'end_date',
    ]
