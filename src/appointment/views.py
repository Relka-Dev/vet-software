from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from appointment.models import Appointment, Room, EmergencyType
from animal.models import Animal
from employee.models import Employee
from .forms import AppointmentForm, ItemFormset, ProcedureFormset, EquipmentFormset
from django.core.exceptions import ValidationError
from django.contrib import messages


def calendar_view(request, year=None, month=None, day=None):
    if year and month and day:
        selected_date = timezone.make_aware(datetime(year, month, day))
    else:
        selected_date = timezone.now()

    selected_date = selected_date.replace(hour=0, minute=0, second=0, microsecond=0)
    next_day = selected_date + timedelta(days=1)
    prev_day = selected_date - timedelta(days=1)

    # Récupérer l'employé connecté et son rôle
    current_employee = None
    user_role = None
    is_reception = False

    if request.user.is_authenticated:
        try:
            current_employee = Employee.objects.select_related('role', 'person').get(
                person=request.user
            )
            user_role = current_employee.role.name
            is_reception = user_role == 'Réceptionniste'
        except Employee.DoesNotExist:
            pass

    # Filtrage des rendez-vous
    if request.user.is_authenticated:
        appointments = Appointment.objects.filter(
            start_date__lt=next_day, end_date__gte=selected_date
        ).select_related('animal', 'employee', 'room', 'emergency_type')

        # Si pas réception, filtrer par employé
        if current_employee and not is_reception:
            appointments = appointments.filter(employee=current_employee)
    else:
        appointments = Appointment.objects.none()

    appointments_with_duration = []
    for appt in appointments:
        duration_minutes = (appt.end_date - appt.start_date).total_seconds() / 60
        height_px = int((duration_minutes / 60) * 56)
        appointments_with_duration.append(
            {
                'appointment': appt,
                'height_px': height_px,
            }
        )

    hours = range(8, 24)
    animals = Animal.objects.all()
    rooms = Room.objects.select_related('room_type').all()

    if is_reception:
        employees = Employee.objects.select_related('person', 'role').all()
    else:
        employees = (
            Employee.objects.select_related('person', 'role').filter(
                id=current_employee.id
            )
            if current_employee
            else []
        )

    emergency_types = EmergencyType.objects.all()

    context = {
        'selected_date': selected_date,
        'prev_day': prev_day,
        'next_day': next_day,
        'hours': hours,
        'appointments': appointments_with_duration,
        'animals': animals,
        'rooms': rooms,
        'employees': employees,
        'emergency_types': emergency_types,
        'is_reception': is_reception,
        'current_employee': current_employee,
    }

    return render(request, 'appointment/calendar.html', context)


def add_appointment(request):
    if request.method == 'POST':
        try:
            current_employee = Employee.objects.select_related('role').get(
                person=request.user
            )
            is_reception = current_employee.role.name == 'Réceptionniste'

            if is_reception:
                employee_id = request.POST.get('employee')
            else:
                employee_id = current_employee.id

            appointment = Appointment(
                animal=Animal.objects.get(id=request.POST.get('animal')),
                room=Room.objects.get(id=request.POST.get('room')),
                employee=Employee.objects.get(id=employee_id),
                emergency_type=EmergencyType.objects.get(
                    id=request.POST.get('emergency_type')
                ),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
            )
            appointment.full_clean()
            appointment.save()
            messages.success(request, "Rendez-vous créé avec succès !")

        except ValidationError as e:
            if hasattr(e, 'messages'):
                for msg in e.messages:
                    messages.error(request, msg)
            else:
                messages.error(request, str(e))
        except Employee.DoesNotExist:
            pass

    return redirect('calendar')


def update_appointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)

    try:
        current_employee = Employee.objects.select_related('role').get(
            person=request.user
        )
        is_reception = current_employee.role.name == 'Réceptionniste'

        if not is_reception and appointment.employee != current_employee:
            return redirect('calendar')
    except Employee.DoesNotExist:
        return redirect('calendar')

    if request.method == 'POST' and 'edit-button' in request.POST:
        try:
            appointment.animal = Animal.objects.get(id=request.POST.get('animal'))
            appointment.room = Room.objects.get(id=request.POST.get('room'))

            if is_reception:
                appointment.employee = Employee.objects.get(id=request.POST.get('employee'))

            appointment.emergency_type = EmergencyType.objects.get(
                id=request.POST.get('emergency_type')
            )
            appointment.start_date = request.POST.get('start_date')
            appointment.end_date = request.POST.get('end_date')
            appointment.full_clean()
            appointment.save()
            messages.success(request, "Rendez-vous modifié avec succès !")
        except ValidationError as e:
            if hasattr(e, 'messages'):
                for msg in e.messages:
                    messages.error(request, msg)
            else:
                messages.error(request, str(e))

    if request.method == 'POST' and 'delete-button' in request.POST:
        appointment.delete()

    return redirect('calendar')


# See all details about items, procedures and equipment used
def appointment_details(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)

    if request.method == 'POST':
        item_form = ItemFormset(request.POST, instance=appointment)
        procedure_form = ProcedureFormset(request.POST, instance=appointment)
        equipment_form = EquipmentFormset(request.POST, instance=appointment)
        if (
            form.is_valid()
            and item_form.is_valid()
            and procedure_form.is_valid()
            and equipment_form.is_valid()
        ):
            item_form.save()
            procedure_form.save()
            equipment_form.save()
            return redirect('appointment_details', pk=appointment.pk)
    else:
        form = AppointmentForm(instance=appointment)
        item_form = ItemFormset(instance=appointment)
        procedure_form = ProcedureFormset(instance=appointment)
        equipment_form = EquipmentFormset(instance=appointment)

    return render(
        request,
        'appointment/appointment_view.html',
        {
            'appointment': appointment,
            'form': form,
            'item_formset': item_form,
            'procedure_formset': procedure_form,
            'equipment_formset': equipment_form,
        },
    )
