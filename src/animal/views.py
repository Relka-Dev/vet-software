from django.shortcuts import render
from .models import Animal, SOAPNote


def animal_list(request):
    animals = Animal.objects.all()
    return render(request, 'animal/animal_list.html', {'animals': animals})


def display_animal_note(request, pk):
    try:
        if pk:
            animal_note = SOAPNote.objects.get(animal__pk=pk)
    except SOAPNote.DoesNotExist:
        animal_note = None

    return render(request, 'animal/animal_note.html', {'animal_note': animal_note})
