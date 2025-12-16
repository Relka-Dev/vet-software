from django.contrib import admin
from .models import Family, Extra_family_member

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ['main_contact', 'creation_date']

@admin.register(Extra_family_member)
class ExtraFamilyMemberAdmin(admin.ModelAdmin):
    list_display = ['family', 'person']
