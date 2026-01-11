from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from datetime import date, timedelta, datetime
from appointment.models import Appointment
from employee.models import OpenHours, AvailabilityEmployee, Employee
import json
from django.contrib.auth.decorators import login_required


def get_appointments_data(year_start, year_end, months):
    appointments_year = (
        Appointment.objects.filter(
            start_date__date__gte=year_start, start_date__date__lte=year_end
        )
        .values('start_date__month')
        .annotate(count=Count('id'))
        .order_by('start_date__month')
    )

    months_label = []
    counts_month = []

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

    return json.dumps({'dates': months_label, 'counts': counts_month}), sum(
        counts_month
    )


def get_room_usage(year_start, year_end):
    today = timezone.now().date()

    # get hours per day of week for the selected year
    hours_per_day_of_week = {}
    for open_hour in OpenHours.objects.filter(
        start_date__lte=year_end, end_date__gte=year_start
    ):
        day_num = open_hour.day_of_week
        if day_num not in hours_per_day_of_week:
            hours_per_day_of_week[day_num] = 0

        start_dt = datetime.combine(date.today(), open_hour.start_time)
        end_dt = datetime.combine(date.today(), open_hour.end_time)
        hours = (end_dt - start_dt).total_seconds() / 3600
        hours_per_day_of_week[day_num] += hours

    # calculate total available hours
    total_hours_available = 0
    current_date = year_start
    while current_date <= min(today, year_end):
        day_of_week = current_date.weekday()  # 0=Monday, 6=Sunday
        if day_of_week in hours_per_day_of_week:
            total_hours_available += hours_per_day_of_week[day_of_week]
        current_date += timedelta(days=1)

    # Calculate room usage hours
    room_usage_hours = {}
    for appointment in Appointment.objects.filter(
        start_date__date__gte=year_start, start_date__date__lte=min(today, year_end)
    ):
        room = appointment.room.room_type.name
        duration_hours = (
            appointment.end_date - appointment.start_date
        ).total_seconds() / 3600

        if room not in room_usage_hours:
            room_usage_hours[room] = 0
        room_usage_hours[room] += duration_hours

    # Calculate room usage percentages
    room_usage_percentage = {}
    for room, hours_used in room_usage_hours.items():
        if total_hours_available > 0:
            percentage = (hours_used / total_hours_available) * 100
            room_usage_percentage[room] = round(percentage, 2)
        else:
            room_usage_percentage[room] = 0

    # Calculate global room usage
    total_hours_used = sum(room_usage_hours.values())
    num_rooms = len(room_usage_hours) if room_usage_hours else 1
    total_hours_available_all_rooms = total_hours_available * num_rooms

    global_room_usage = (
        (total_hours_used / total_hours_available_all_rooms) * 100
        if total_hours_available_all_rooms > 0
        else 0
    )

    return json.dumps(room_usage_percentage), round(global_room_usage, 2)


def get_vet_utilization(year_start, year_end):
    today = timezone.now().date()

    veterinarians = Employee.objects.filter(role__name="Vétérinaire")
    vet_usage_percentage = {}

    # get hours per day of week for each vet
    for vet in veterinarians:
        hours_per_day_of_week = {}
        for availability in AvailabilityEmployee.objects.filter(
            employee=vet, start_date__lte=year_end, end_date__gte=year_start
        ):
            day_num = availability.day_of_week
            if day_num not in hours_per_day_of_week:
                hours_per_day_of_week[day_num] = 0

            start_dt = datetime.combine(date.today(), availability.start_time)
            end_dt = datetime.combine(date.today(), availability.end_time)
            hours = (end_dt - start_dt).total_seconds() / 3600
            hours_per_day_of_week[day_num] += hours

        total_hours_available = 0
        current_date = year_start
        while current_date <= min(today, year_end):
            day_of_week = current_date.weekday()
            if day_of_week in hours_per_day_of_week:
                total_hours_available += hours_per_day_of_week[day_of_week]
            current_date += timedelta(days=1)

        # Calculate hours worked from appointments
        hours_worked = 0
        for appointment in Appointment.objects.filter(
            employee=vet,
            start_date__date__gte=year_start,
            start_date__date__lte=min(today, year_end),
        ):
            duration_hours = (
                appointment.end_date - appointment.start_date
            ).total_seconds() / 3600
            hours_worked += duration_hours

        vet_name = str(vet.person)
        if total_hours_available > 0:
            percentage = (hours_worked / total_hours_available) * 100
            vet_usage_percentage[vet_name] = round(percentage, 2)
        else:
            vet_usage_percentage[vet_name] = 0

    # Calculate global vet utilization
    global_vet_usage = 0
    if len(vet_usage_percentage) > 0:
        global_vet_usage = sum(vet_usage_percentage.values()) / len(
            vet_usage_percentage
        )

    return vet_usage_percentage, round(global_vet_usage, 2)


@login_required
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

    if year is None:
        selected_year = today.year
    else:
        selected_year = int(year)

    # use December for 2025, if not use full year
    if selected_year == 2025:
        year_start = timezone.now().replace(year=selected_year, month=12, day=1).date()
        year_end = timezone.now().replace(year=selected_year, month=12, day=31).date()
    else:
        year_start = timezone.now().replace(year=selected_year, month=1, day=1).date()
        year_end = timezone.now().replace(year=selected_year, month=12, day=31).date()

    appointments_data, total_appointments = get_appointments_data(
        year_start, year_end, months
    )

    room_usage_percentage, global_room_usage = get_room_usage(year_start, year_end)

    vet_usage_percentage, global_vet_usage = get_vet_utilization(year_start, year_end)

    context = {
        'appointments_data': appointments_data,
        'total_appointments': total_appointments,
        'current_year': selected_year,
        'room_usage_percentage': room_usage_percentage,
        'global_room_usage': global_room_usage,
        'vet_usage_percentage': vet_usage_percentage,
        'global_vet_usage': global_vet_usage,
    }

    return render(request, 'dashboard/dashboard.html', context)
