from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta

from appointment.models import Appointment


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

    context = {
        'selected_date': selected_date,
        'prev_day': prev_day,
        'next_day': next_day,
        'hours': hours,
        'appointments': appointments_with_duration,
    }

    return render(request, 'appointment/calendar.html', context)
