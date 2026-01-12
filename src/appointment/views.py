from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from appointment.models import (
    Appointment,
    Room,
    EmergencyType,
    AppointmentItem,
    AppointmentProcedure,
)
from animal.models import Animal
from employee.models import Employee
from .forms import AppointmentForm, ItemFormset, ProcedureFormset, EquipmentFormset
import io
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from .utils import get_reminders
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages


@login_required
def calendar_view(request, year=None, month=None, day=None):
    if year and month and day:
        selected_date = timezone.make_aware(datetime(year, month, day))
    else:
        selected_date = timezone.now()

    selected_date = selected_date.replace(hour=0, minute=0, second=0, microsecond=0)
    next_day = selected_date + timedelta(days=1)
    prev_day = selected_date - timedelta(days=1)

    # Récupérer l'employé connecté et son rôle
    current_employee = None
    user_role = None
    is_reception = False

    if request.user.is_authenticated:
        try:
            current_employee = Employee.objects.select_related('role', 'person').get(
                person=request.person
            )
            user_role = current_employee.role.name
            is_reception = user_role == 'Réceptionniste'
        except Employee.DoesNotExist:
            pass

    # Filtrage des rendez-vous
    if request.user.is_authenticated:
        appointments = Appointment.objects.filter(
            start_date__lt=next_day, end_date__gte=selected_date
        ).select_related('animal', 'employee', 'room', 'emergency_type')

        # Si pas réception, filtrer par employé
        if current_employee and not is_reception:
            appointments = appointments.filter(employee=current_employee)
    else:
        appointments = Appointment.objects.none()

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

    if is_reception:
        employees = Employee.objects.select_related('person', 'role').all()
    else:
        employees = (
            Employee.objects.select_related('person', 'role').filter(
                id=current_employee.id
            )
            if current_employee
            else []
        )

    emergency_types = EmergencyType.objects.all()

    reminders_of_today = [
        r for r in get_reminders() if r['reminder_date'] == timezone.now().date()
    ]

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
        'is_reception': is_reception,
        'current_employee': current_employee,
        'reminders_of_today': reminders_of_today,
    }

    return render(request, 'appointment/calendar.html', context)


def reminder_list(request):
    reminders = get_reminders()
    reminders_today = []
    reminders_rest = []

    for r in reminders:
        if r['reminder_date'] == timezone.now().date():
            reminders_today.append(r)
        else:
            reminders_rest.append(r)

    context = {
        'reminders': reminders,
        'reminders_today': reminders_today,
        'reminders_rest': reminders_rest,
    }

    return render(request, 'appointment/reminder_list.html', context)


@login_required
def add_appointment(request):
    if request.method == 'POST':
        try:
            current_employee = Employee.objects.select_related('role').get(
                person=request.person
            )
            is_reception = current_employee.role.name == 'Réceptionniste'

            if is_reception:
                employee_id = request.POST.get('employee')
            else:
                employee_id = current_employee.id

            appointment = Appointment(
                animal=Animal.objects.get(id=request.POST.get('animal')),
                room=Room.objects.get(id=request.POST.get('room')),
                employee=Employee.objects.get(id=employee_id),
                emergency_type=EmergencyType.objects.get(
                    id=request.POST.get('emergency_type')
                ),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
            )
            appointment.full_clean()
            appointment._current_user = request.person
            appointment.save()
            messages.success(request, "Rendez-vous créé avec succès !")

        except ValidationError as e:
            if hasattr(e, 'messages'):
                for msg in e.messages:
                    messages.error(request, msg)
            else:
                messages.error(request, str(e))
        except Employee.DoesNotExist:
            pass

    return redirect('calendar')


@login_required
def update_appointment(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)

    try:
        current_employee = Employee.objects.select_related('role').get(
            person=request.person
        )
        is_reception = current_employee.role.name == 'Réceptionniste'

        if not is_reception and appointment.employee != current_employee:
            return redirect('calendar')
    except Employee.DoesNotExist:
        return redirect('calendar')

    if request.method == 'POST' and 'edit-button' in request.POST:
        try:
            appointment.animal = Animal.objects.get(id=request.POST.get('animal'))
            appointment.room = Room.objects.get(id=request.POST.get('room'))

            if is_reception:
                appointment.employee = Employee.objects.get(
                    id=request.POST.get('employee')
                )

            appointment.emergency_type = EmergencyType.objects.get(
                id=request.POST.get('emergency_type')
            )
            appointment.start_date = request.POST.get('start_date')
            appointment.end_date = request.POST.get('end_date')
            appointment._current_user = request.person
            appointment.full_clean()
            appointment.save()
        except ValidationError as e:
            if hasattr(e, 'messages'):
                for msg in e.messages:
                    messages.error(request, msg)
            else:
                messages.error(request, str(e))

    if request.method == 'POST' and 'delete-button' in request.POST:
        appointment._current_user = request.person
        appointment.delete()

    return redirect('calendar')


@login_required
# See all details about items, procedures and equipment used
def appointment_details(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)

    if request.method == 'POST':
        item_form = ItemFormset(request.POST, instance=appointment)
        procedure_form = ProcedureFormset(request.POST, instance=appointment)
        equipment_form = EquipmentFormset(request.POST, instance=appointment)
        if (
            item_form.is_valid()
            and procedure_form.is_valid()
            and equipment_form.is_valid()
        ):

            for form in item_form:
                if form.cleaned_data:
                    form.instance._current_user = request.person
            for form in procedure_form:
                if form.cleaned_data:
                    form.instance._current_user = request.person
            for form in equipment_form:
                if form.cleaned_data:
                    form.instance._current_user = request.person

            item_form.save()
            procedure_form.save()
            equipment_form.save()
            return redirect('appointment_details', pk=appointment.pk)
    else:
        form = AppointmentForm(instance=appointment)
        item_form = ItemFormset(instance=appointment)
        procedure_form = ProcedureFormset(instance=appointment)
        equipment_form = EquipmentFormset(instance=appointment)

    return render(
        request,
        'appointment/appointment_view.html',
        {
            'appointment': appointment,
            'form': form,
            'item_formset': item_form,
            'procedure_formset': procedure_form,
            'equipment_formset': equipment_form,
        },
    )


# Generate a invoice with total items and procedures used
def generate_invoice_pdf(request, pk):
    appointment = get_object_or_404(
        Appointment.objects.select_related(
            'animal', 'employee', 'room', 'emergency_type'
        ),
        id=pk,
    )

    # Baseline
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 2 * cm

    # Header
    p.setFont("Helvetica-Bold", 20)
    p.drawString(2 * cm, y, "FACTURE")
    p.setFont("Helvetica", 10)
    y -= 0.5 * cm
    p.drawString(2 * cm, y, f"Date: {datetime.now().strftime('%d/%m/%Y')}")
    y -= 0.4 * cm
    p.drawString(2 * cm, y, f"N° Facture: INV-{appointment.id:05d}")

    # Separation line
    y -= 1 * cm
    p.line(2 * cm, y, width - 2 * cm, y)

    # General informations
    y -= 1 * cm
    p.setFont("Helvetica-Bold", 12)
    p.drawString(2 * cm, y, "Détails du rendez-vous")

    y -= 0.7 * cm
    p.setFont("Helvetica", 10)
    p.drawString(2 * cm, y, f"Animal: {appointment.animal.name}")
    y -= 0.5 * cm
    p.drawString(
        2 * cm,
        y,
        f"Date et heure: {appointment.start_date.strftime('%d/%m/%Y %H:%M')} - {appointment.end_date.strftime('%H:%M')}",
    )
    y -= 0.5 * cm
    p.drawString(2 * cm, y, f"Vétérinaire: {appointment.employee}")
    y -= 0.5 * cm
    p.drawString(2 * cm, y, f"Salle: {appointment.room}")
    y -= 0.5 * cm
    p.drawString(2 * cm, y, f"Type de rendez-vous: {appointment.emergency_type}")

    # Separation line
    y -= 0.8 * cm
    p.line(2 * cm, y, width - 2 * cm, y)

    # Table for item/procedure
    y -= 1 * cm
    p.setFont("Helvetica-Bold", 12)
    p.drawString(2 * cm, y, "Détails de la facturation")

    # Table data
    data = [['Description', 'Quantité', 'Prix unitaire', 'Total']]
    total_general = 0

    # Fetch all items and calculate total with price + quantity
    items = AppointmentItem.objects.filter(appointment=appointment).select_related(
        'item'
    )
    for item in items:
        prix_unitaire = item.item.price
        total_ligne = prix_unitaire * item.quantity
        total_general += total_ligne
        data.append(
            [
                str(item.item),
                str(item.quantity),
                f"{prix_unitaire:.2f} CHF",
                f"{total_ligne:.2f} CHF",
            ]
        )

    # Fetch all procedures and calculate total with price + quantity
    procedures = AppointmentProcedure.objects.filter(
        appointment=appointment
    ).select_related('procedure')
    for proc in procedures:
        prix_unitaire = proc.procedure.price
        total_ligne = prix_unitaire * proc.quantity
        total_general += total_ligne
        data.append(
            [
                str(proc.procedure.name),
                str(proc.quantity),
                f"{prix_unitaire:.2f} CHF",
                f"{total_ligne:.2f} CHF",
            ]
        )

    # If no item/procedure
    if len(data) == 1:
        data.append(['Aucun article ou procédure', '-', '-', '-'])

    # Create table
    y -= 0.5 * cm
    table = Table(data, colWidths=[8 * cm, 2 * cm, 3 * cm, 3 * cm])
    table.setStyle(
        TableStyle(
            [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ]
        )
    )

    # Draw table
    table.wrapOn(p, width, height)
    table_height = table._height
    table.drawOn(p, 2 * cm, y - table_height)

    # Total
    y = y - table_height - 1 * cm
    p.line(width - 8 * cm, y, width - 2 * cm, y)
    y -= 0.5 * cm
    p.setFont("Helvetica-Bold", 12)
    p.drawString(width - 8 * cm, y, "TOTAL:")
    p.drawRightString(width - 2 * cm, y, f"{total_general:.2f} CHF")

    # Footer
    p.setFont("Helvetica", 8)
    p.drawCentredString(width / 2, 1.5 * cm, "Merci de votre confiance")
    p.drawCentredString(width / 2, 1 * cm, "Clinique Vétérinaire - Votre adresse ici")

    # Finalize file
    p.showPage()
    p.save()
    buffer.seek(0)
    filename = f"facture_{appointment.id}_{appointment.animal.name}_{datetime.now().strftime('%Y%m%d')}.pdf"
    return FileResponse(buffer, as_attachment=True, filename=filename)
