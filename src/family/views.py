from django.shortcuts import render, redirect, get_object_or_404
from .models import Family, Extra_family_member
from .forms import PersonForm
from person.models import Person


def family_list(request):
    families = Family.objects.all()
    return render(request, 'family/family_list.html', {'families': families})


def family_contacts(request, pk):
    try:
        if pk:
            family = Family.objects.get(pk=pk)
            family_main_contact = family.main_contact
            family_contacts = family.extra.all()
    except Family.DoesNotExist:
        family = None
        family_main_contact = None
        family_contacts = []

    return render(
        request,
        'family/family_details.html',
        {
            'family': family,
            'family_main_contact': family_main_contact,
            'family_contacts': family_contacts,
        },
    )


# Add a family (= creates a Person as main_contact)
def add_family(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save()
            family = Family.objects.create(main_contact=person)

            return redirect('family_contacts', pk=family.pk)
    else:
        form = PersonForm()

    return render(request, 'family/family_list.html', {'form': form})


# Add (=create) an extra member to an existing family
def add_family_member(request, family_pk):
    family = get_object_or_404(Family, pk=family_pk)

    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save()
            Extra_family_member.objects.create(family=family, person=person)

            return redirect('family_contacts', pk=family.pk)
    else:
        form = PersonForm()

    context = {
        'form': form,
        'family': family,
    }
    return render(request, 'family/family_details.html', context)


# Edit any family member (main contact or extra member)
def edit_family_member(request, family_pk, person_pk):
    family = get_object_or_404(Family, pk=family_pk)
    person = get_object_or_404(Person, pk=person_pk)

    # Check if this person belongs to this family
    is_main_contact = family.main_contact == person
    is_extra_member = Extra_family_member.objects.filter(
        family=family, person=person
    ).exists()

    if not (is_main_contact or is_extra_member):
        return redirect('family_contacts', pk=family_pk)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('family_contacts', pk=family_pk)
    else:
        form = PersonForm(instance=person)

    context = {
        'form': form,
        'family': family,
        'person': person,
        'is_main_contact': is_main_contact,
    }
    return render(request, 'family/family_details.html', context)


# Delete family member
def delete_family_member(request, member_pk):
    extra_member = get_object_or_404(Extra_family_member, pk=member_pk)
    family_pk = extra_member.family.pk

    if request.method == 'POST':
        extra_member.person.delete()  # This will also delete the extra_member due to CASCADE
        return redirect('family_contacts', pk=family_pk)

    context = {
        'extra_member': extra_member,
    }
    return render(request, 'family/family_details.html', context)
