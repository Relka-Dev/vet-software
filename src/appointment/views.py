from django.shortcuts import render


def calendar_view(request):
    return render(request, 'appointment/calendar.html')
