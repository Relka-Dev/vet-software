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


def animal_family_contacts(request, pk):
    try:
        if pk:
            animal = Animal.objects.get(pk=pk)
            family_main_contact = animal.family.main_contact
            family_contacts = animal.family.extra.all()
    except Animal.DoesNotExist:
        animal = None
        family_main_contact = None
        family_contacts = []

    return render(
        request,
        'animal/animal_family_contacts.html',
        {
            'animal': animal,
            'family_main_contact': family_main_contact,
            'family_contacts': family_contacts,
        },
    )
