from datetime import timedelta
from django.utils import timezone
from appointment.models import AppointmentItem


# Get all items which has a reminder
def get_reminders():
    all_reminders = []
    appointment_items = (
        AppointmentItem.objects.filter(item__reminder=True)
        .select_related('appointment__animal', 'appointment__employee', 'item')
        .order_by('-appointment__start_date')
    )
    for app_item in appointment_items:
        reminder_date = app_item.appointment.start_date.date() + timedelta(days=30)

        reminder = {
            'id': f"{app_item.id}",
            'animal': app_item.appointment.animal,
            'item': app_item.item,
            'appointment': app_item.appointment,
            'reminder_date': reminder_date,
            'original_date': app_item.appointment.start_date.date(),
        }

        all_reminders.append(reminder)

    all_reminders.sort(key=lambda x: x['reminder_date'])
    return all_reminders
