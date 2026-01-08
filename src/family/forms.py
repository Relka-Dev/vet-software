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
            'last_name': 'Prénom',
            'first_name': 'Nom',
            'phone': 'Téléphone',
            'email': 'Email',
            'birthday': 'Date de naissance',
        }
        widgets = {
            'last_name': forms.TextInput(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                }
            ),
            'phone': forms.NumberInput(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                }
            ),
            'birthday': forms.DateTimeInput(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                }
            ),
        }
