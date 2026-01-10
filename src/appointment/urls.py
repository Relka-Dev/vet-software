from django.urls import path
from . import views

urlpatterns = [
    path('calendar/', views.calendar_view, name='calendar'),
    path(
        'calendar/<int:year>/<int:month>/<int:day>/',
        views.calendar_view,
        name='calendar_date',
    ),
    path('calendar/add/', views.add_appointment, name='add_appointment'),
    path(
        'calendar/update/<int:pk>/', views.update_appointment, name='update_appointment'
    ),
    path(
        'calendar/details/<int:pk>/',
        views.appointment_details,
        name='appointment_details',
    ),
    path(
        'calendar/details/<int:pk>/invoice',
        views.generate_invoice_pdf,
        name="generate_invoice",
    ),
]
