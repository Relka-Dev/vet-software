from django.contrib import admin
from .models import Animal, AnimalChart

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['name', 'birthday', 'federal_identification', 'family']
    list_filter = ['name', 'family']
    search_fields = ['name', 'family', 'identification']

@admin.register(AnimalChart)
class AnimalChartAdmin(admin.ModelAdmin):
    list_display = ['animal']
