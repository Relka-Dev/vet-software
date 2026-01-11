from pyexpat.errors import messages
from click import edit
from django.shortcuts import redirect, render

from family.models import Family
from .models import Animal, SOAPNote, Species
from .forms import SOAPNoteForm
from django.contrib.auth.decorators import login_required


@login_required
def animal_list(request):
    animals = Animal.objects.all()
    families = Family.objects.all()
    species = Species.objects.all()
    return render(
        request,
        'animal/animal_list.html',
        {'animals': animals, 'families': families, 'species': species},
    )


@login_required
def display_animal_note(request, animal_pk, note_pk):
    animal = None
    animal_note = None
    animal_notes = []
    form = None
    new_form = None

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

    if request.method == 'POST':
        is_new_note = request.POST.get('action') == 'new'

        if is_new_note:
            form = SOAPNoteForm(request.POST)
            if form.is_valid():
                new_note = form.save(commit=False)
                new_note.animal = animal
                new_note._current_user = request.person
                new_note.save()
                return redirect('animal_note', animal_pk=animal.id, note_pk=new_note.id)
        else:
            form = SOAPNoteForm(request.POST, instance=animal_note)
            if form.is_valid() and 'edit-button' in request.POST:
                if animal_note.validated_by:
                    messages.error(
                        request,
                        "Ce rendez-vous est déjà validé et ne peut plus être modifié.",
                    )
                    return redirect(
                        'animal_note', animal_pk=animal.id, note_pk=animal_note.id
                    )
                instance = form.save(commit=False)
                instance._current_user = request.person
                instance.save()
                return redirect(
                    'animal_note', animal_pk=animal.id, note_pk=animal_note.id
                )
            elif form.is_valid() and 'delete-button' in request.POST:
                animal_note._current_user = request.person
                animal_note.delete()
                return redirect('animal_note_by_animal', animal_pk=animal.id)
            new_form = SOAPNoteForm(user=request.person)
    else:
        form = SOAPNoteForm(instance=animal_note)
        new_form = SOAPNoteForm()

    return render(
        request,
        'animal/animal_note.html',
        {
            'animal': animal,
            'animal_note': animal_note,
            'animal_notes': animal_notes,
            'form': form,
            'new_form': new_form,
        },
    )


@login_required
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


@login_required
def add_animal(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        birthday = request.POST.get('birthday')
        federal_identification = request.POST.get('federal_identification')
        family_id = request.POST.get('family')
        family = Family.objects.get(pk=family_id)
        species_id = request.POST.get('species')
        species = Species.objects.get(pk=species_id)

        animal = Animal(
            name=name,
            birthday=birthday,
            federal_identification=federal_identification,
            family=family,
            species=species,
        )
        animal._current_user = request.person
        animal.save()

    return redirect('animal_list')


@login_required
def update_animal(request, pk):
    animal = Animal.objects.get(id=pk)

    if request.method == 'POST' and 'edit-button' in request.POST:
        animal.name = request.POST.get('name')
        animal.birthday = request.POST.get('birthday')
        animal.federal_identification = request.POST.get('federal_identification')
        family_id = request.POST.get('family')
        species_id = request.POST.get('species')
        animal.family = Family.objects.get(id=family_id)
        animal.species = Species.objects.get(id=species_id)
        animal._current_user = request.person
        animal.save()
        return redirect('animal_list')

    if request.method == 'POST' and 'delete-button' in request.POST:
        animal._current_user = request.person
        animal.delete()
        return redirect('animal_list')

    return render(request, 'animal/animal_list.html', {'animal': animal})
