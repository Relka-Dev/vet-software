from django import forms
from .models import (
    Appointment,
    AppointmentItem,
    AppointmentProcedure,
    AppointmentEquipment,
)

COMMON_INPUT_CLASS = ' border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5 mt-1.5 focus:ring-gray-500 focus:border-gray-500'


# Create an appointment form
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'animal',
            'employee',
            'room',
            'emergency_type',
            'start_date',
            'end_date',
        ]
        labels = {
            'animal': "Animal",
            'employee': "Employé",
            'room': "Salle",
            'emergency_type': "Type d'urgence",
            'start_date': "Date de début",
            'end_date': "Date de fin",
        }
        widgets = {
            'animal': forms.Select(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                    'placeholder': "Sélectionner un animal...",
                }
            ),
            'employee': forms.Select(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                    'placeholder': "Sélectionner un employé...",
                }
            ),
            'room': forms.Select(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                    'placeholder': "Sélectionner une salle...",
                }
            ),
            'emergency_type': forms.Select(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                    'placeholder': "Sélectionner un type d'urgence...",
                }
            ),
            'start_date': forms.DateTimeInput(
                attrs={'class': COMMON_INPUT_CLASS, 'type': 'datetime-local'}
            ),
            'end_date': forms.DateTimeInput(
                attrs={'class': COMMON_INPUT_CLASS, 'type': 'datetime-local'}
            ),
        }


# Create a form for item in an appointment
class ItemForm(forms.ModelForm):
    class Meta:
        model = AppointmentItem
        fields = ['item', 'quantity']
        labels = {
            'item': "Article",
            'quantity': "Quantité",
        }
        widgets = {
            'item': forms.Select(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                    'placeholder': "Sélectionner un article...",
                }
            ),
            'quantity': forms.NumberInput(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                    'placeholder': "Entrer la quantité...",
                }
            ),
        }


# Create a form for procedures in an appointment
class ProcedureForm(forms.ModelForm):
    class Meta:
        model = AppointmentProcedure
        fields = ['procedure', 'quantity']
        labels = {
            'procedure': "Procédure",
            'quantity': "Quantité",
        }
        widgets = {
            'procedure': forms.Select(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                    'placeholder': "Sélectionner la procédure...",
                }
            ),
            'quantity': forms.NumberInput(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                    'placeholder': "Entrer la quantité...",
                }
            ),
        }


# Create a form for equipments in an appointment
class EquipmentForm(forms.ModelForm):
    class Meta:
        model = AppointmentEquipment
        fields = ['equipment']
        labels = {
            'equipment': "Équipement",
        }
        widgets = {
            'equipment': forms.Select(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                    'placeholder': "Sélectionner l'équipement...",
                }
            ),
        }


# Create all the Formset to link an appointment to each elements (item, procedure, equipment)
ItemFormset = forms.inlineformset_factory(
    Appointment, AppointmentItem, form=ItemForm, extra=1, can_delete=True
)
ProcedureFormset = forms.inlineformset_factory(
    Appointment, AppointmentProcedure, form=ProcedureForm, extra=1, can_delete=True
)
EquipmentFormset = forms.inlineformset_factory(
    Appointment, AppointmentEquipment, form=EquipmentForm, extra=1, can_delete=True
)
