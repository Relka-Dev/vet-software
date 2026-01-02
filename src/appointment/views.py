from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from appointment.models import Appointment, Room, EmergencyType
from animal.models import Animal
from employee.models import Employee


def calendar_view(request, year=None, month=None, day=None):
    if year and month and day:
        selected_date = timezone.make_aware(datetime(year, month, day))
    else:
        selected_date = timezone.now()

    selected_date = selected_date.replace(hour=0, minute=0, second=0, microsecond=0)
    next_day = selected_date + timedelta(days=1)
    prev_day = selected_date - timedelta(days=1)

    appointments = Appointment.objects.filter(
        start_date__lt=next_day, end_date__gte=selected_date
    ).select_related('animal', 'employee', 'room', 'emergency_type')

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
    employees = Employee.objects.select_related('person', 'role').all()
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
    }

    return render(request, 'appointment/calendar.html', context)


def add_appointment(request):
    if request.method == 'POST':
        Appointment.objects.create(
            animal=Animal.objects.get(id=request.POST.get('animal')),
            room=Room.objects.get(id=request.POST.get('room')),
            employee=Employee.objects.get(id=request.POST.get('employee')),
            emergency_type=EmergencyType.objects.get(id=request.POST.get('emergency_type')),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date')
        )
    return redirect('calendar')


def update_appointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)

    if request.method == 'POST' and 'edit-button' in request.POST:
        appointment.animal = Animal.objects.get(id=request.POST.get('animal'))
        appointment.room = Room.objects.get(id=request.POST.get('room'))
        appointment.employee = Employee.objects.get(id=request.POST.get('employee'))
        appointment.emergency_type = EmergencyType.objects.get(id=request.POST.get('emergency_type'))
        appointment.start_date = request.POST.get('start_date')
        appointment.end_date = request.POST.get('end_date')
        appointment.save()

    if request.method == 'POST' and 'delete-button' in request.POST:
        appointment.delete()

    return redirect('calendar')
