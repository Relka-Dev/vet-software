from django.shortcuts import render
from .models import Animal, SOAPNote
from .forms import SOAPNoteForm


def animal_list(request):
    animals = Animal.objects.all()
    return render(request, 'animal/animal_list.html', {'animals': animals})


def display_animal_note(request, animal_pk, note_pk):
    animal = None
    animal_note = None
    animal_notes = []
    form = None

    if note_pk:
        try:
            animal_note = SOAPNote.objects.get(pk=note_pk)
            animal = animal_note.animal
            animal_notes = SOAPNote.objects.filter(animal=animal).order_by(
                '-created_at'
            )
        except SOAPNote.DoesNotExist:
            pass
    elif animal_pk:
        try:
            animal = Animal.objects.get(pk=animal_pk)
            animal_notes = SOAPNote.objects.filter(animal=animal).order_by(
                '-created_at'
            )
            if animal_notes.exists():
                animal_note = animal_notes.first()
        except Animal.DoesNotExist:
            pass

    if request.method == 'POST' and animal_note:
        form = SOAPNoteForm(request.POST, instance=animal_note)
        if form.is_valid():
            form.save()
    else:
        form = SOAPNoteForm(instance=animal_note)

    return render(
        request,
        'animal/animal_note.html',
        {
            'animal': animal,
            'animal_note': animal_note,
            'animal_notes': animal_notes,
            'form': form,
        },
    )


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
