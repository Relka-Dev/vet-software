from django import forms
from .models import Family, Extra_family_member
from person.models import Person

COMMON_INPUT_CLASS = ' border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5 mt-1.5 focus:ring-gray-500 focus:border-gray-500'


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'last_name',
            'first_name',
            'phone',
            'email',
            'birthday',
        ]
        labels = {
            'last_name': 'Nom',
            'first_name': 'Prénom',
            'phone': 'Téléphone',
            'email': 'Email',
            'birthday': 'Date de naissance',
        }
        widgets = {
            'last_name': forms.TextInput(
                attrs={'class': COMMON_INPUT_CLASS, 'placeholder': "Entrer le nom..."}
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                    'placeholder': "Entrer le prénom...",
                }
            ),
            'phone': forms.NumberInput(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                    'placeholder': "Entrer le numéro de téléphone...",
                }
            ),
            'email': forms.TextInput(
                attrs={'class': COMMON_INPUT_CLASS, 'placeholder': "Entrer l'email..."}
            ),
            'birthday': forms.DateInput(
                attrs={'class': COMMON_INPUT_CLASS, 'type': "date"}
            ),
        }
