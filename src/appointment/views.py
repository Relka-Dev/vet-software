from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta

from appointment.models import Appointment


def calendar_view(request):
    today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)

    appointments = Appointment.objects.filter(
        start_date__lt=tomorrow, end_date__gte=today
    ).select_related('animal', 'employee', 'room', 'emergency_type')

    hours = range(8, 24)

    context = {
        'today': today,
        'hours': hours,
        'appointments': appointments,
    }

    return render(request, 'appointment/calendar.html', context)
