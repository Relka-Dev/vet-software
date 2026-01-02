from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from appointment.models import Appointment
import json


def dashboard_view(request, year=None):
    today = timezone.now().date()
    months = [
        'Janvier',
        'Février',
        'Mars',
        'Avril',
        'Mai',
        'Juin',
        'Juillet',
        'Août',
        'Septembre',
        'Octobre',
        'Novembre',
        'Décembre',
    ]
    months_label = []
    counts_month = []

    if year is None:
        selected_year = today.year
    else:
        selected_year = int(year)

    year_start = timezone.now().replace(year=selected_year, month=1, day=1).date()
    year_end = timezone.now().replace(year=selected_year, month=12, day=31).date()

    # get appointments by month for the selected year
    appointments_year = (
        Appointment.objects.filter(
            start_date__date__gte=year_start, start_date__date__lte=year_end
        )
        .values('start_date__month')
        .annotate(count=Count('id'))
        .order_by('start_date__month')
    )

    # Calculate room usage %
    num_days = (year_end - year_start).days + 1
    total_hours_available = num_days * 8

    room_usage_hours = {}
    room_usage_percentage = {}

    for appointment in Appointment.objects.filter(
        start_date__date__gte=year_start, start_date__date__lte=year_end
    ):
        room = appointment.room.room_type.name

        # Calculate duration in hours
        duration_hours = (
            appointment.end_date - appointment.start_date
        ).total_seconds() / 3600

        # Add to room hours used
        if room not in room_usage_hours:
            room_usage_hours[room] = 0
        room_usage_hours[room] += duration_hours

    for room, hours_used in room_usage_hours.items():
        percentage = (hours_used / total_hours_available) * 100
        room_usage_percentage[room] = round(percentage, 2)

    for month_num in range(1, 13):
        months_label.append(months[month_num - 1])
        count = next(
            (
                item['count']
                for item in appointments_year
                if item['start_date__month'] == month_num
            ),
            0,
        )
        counts_month.append(count)

    # calculate total room usage %
    total_hours_used = sum(room_usage_hours.values())
    num_rooms = len(room_usage_hours) if room_usage_hours else 1
    total_hours_available_all_rooms = total_hours_available * num_rooms

    global_room_usage = (
        (total_hours_used / total_hours_available_all_rooms) * 100
        if total_hours_available_all_rooms > 0
        else 0
    )

    context = {
        'appointments_data': json.dumps(
            {'dates': months_label, 'counts': counts_month}
        ),
        'total_appointments': sum(counts_month),
        'current_year': selected_year,
        'room_usage_percentage': json.dumps(room_usage_percentage),
        'global_room_usage': round(global_room_usage, 2),
    }

    return render(request, 'dashboard/dashboard.html', context)
