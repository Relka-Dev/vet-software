from django.contrib import admin
from .models import Animal, SOAPNote, Species


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['species', 'name', 'birthday', 'federal_identification', 'family']
    list_filter = ['name', 'family']
    search_fields = ['name', 'family', 'identification']


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(SOAPNote)
class SOAPNoteAdmin(admin.ModelAdmin):
    list_display = [
        'animal',
        'created_at',
        'created_by',
        'validated_by',
    ]
    list_filter = ['created_at', 'created_by', 'validated_by']
