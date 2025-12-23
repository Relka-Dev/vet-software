from django.shortcuts import render
from datetime import date


def calendar_view(request):
    context = {
        'hours': range(0, 24),
    }
    return render(request, 'appointment/calendar.html', context)
