from django.contrib import admin
from .models import RoomType, Room, EmergencyType, Procedure, Equipement, Appointement, Note

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

@admin.register(Equipement)
class EquipementAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Appointement)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['animal', 'room', 'employee', 'emergency_type', 'start_date', 'end_date']

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['appointement', 'created_at', 'created_by', 'validated_by']
