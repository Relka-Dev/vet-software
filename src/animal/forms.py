from django import forms
from .models import SOAPNote

COMMON_INPUT_CLASS = ' border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5 mt-1.5 focus:ring-gray-500 focus:border-gray-500'


class SOAPNoteForm(forms.ModelForm):
    class Meta:
        model = SOAPNote
        fields = [
            'content',
            'text_subjective',
            'text_objective',
            'text_assessment',
            'text_plan',
        ]
        labels = {
            'content': 'Description',
            'text_subjective': 'Subjectif',
            'text_objective': 'Objectif',
            'text_assessment': 'Évaluation',
            'text_plan': 'Plan',
        }
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                    'placeholder': "Entrer une description...",
                }
            ),
            'text_subjective': forms.Textarea(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                    'rows': 4,
                    'placeholder': "Écrire l'observation subjective...",
                }
            ),
            'text_objective': forms.Textarea(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                    'rows': 4,
                    'placeholder': "Écrire l'observation objective...",
                }
            ),
            'text_assessment': forms.Textarea(
                attrs={
                    'class': COMMON_INPUT_CLASS,
                    'rows': 4,
                    'placeholder': "Écrire l'évaluation...",
                }
            ),
            'text_plan': forms.Textarea(
                attrs={
                    'class': COMMON_INPUT_CLASS + ' mb-4',
                    'rows': 4,
                    'placeholder': "Écrire le plan d'action...",
                }
            ),
        }
