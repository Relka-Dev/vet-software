from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from appointment.models import Appointment
import json


def dashboard_view(request, year=None):
    today = timezone.now().date()

    if year is None:
        selected_year = today.year
    else:
        selected_year = int(year)

    year_start = timezone.now().replace(year=selected_year, month=1, day=1).date()
    year_end = timezone.now().replace(year=selected_year, month=12, day=31).date()

    appointments_year = (
        Appointment.objects.filter(
            start_date__date__gte=year_start, start_date__date__lte=year_end
        )
        .values('start_date__month')
        .annotate(count=Count('id'))
        .order_by('start_date__month')
    )

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
    dates_year = []
    counts_year = []

    for month_num in range(1, 13):
        dates_year.append(months[month_num - 1])
        count = next(
            (
                item['count']
                for item in appointments_year
                if item['start_date__month'] == month_num
            ),
            0,
        )
        counts_year.append(count)

    context = {
        'appointments_data': json.dumps({'dates': dates_year, 'counts': counts_year}),
        'total_appointments': sum(counts_year),
        'current_year': selected_year,
    }

    return render(request, 'dashboard/dashboard.html', context)
