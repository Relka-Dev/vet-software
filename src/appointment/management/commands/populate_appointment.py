from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from animal.models import Animal
from employee.models import Employee
from inventory.models import Item
from appointment.models import (
    RoomType,
    Room,
    EmergencyType,
    Procedure,
    Equipment,
    Appointment,
    AppointmentProcedure,
    AppointmentEquipment,
    AppointmentItem,
)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write("Populating appointment data...")

        animals = list(Animal.objects.all())
        if len(animals) < 3:
            self.stdout.write(
                self.style.ERROR("Not enough animals. Run populate_animal.")
            )
            return

        employees = list(Employee.objects.filter(role__name="Vétérinaire"))
        if len(employees) < 2:
            self.stdout.write(
                self.style.ERROR("Not enough veterinarians. Run populate_employee.")
            )
            return

        items = list(Item.objects.all()[:3])
        if len(items) < 3:
            self.stdout.write(
                self.style.ERROR("Not enough items. Run populate_inventory.")
            )
            return

        # Create Room Types
        room_type_consultation = RoomType.objects.create(name="Consultation")
        room_type_surgery = RoomType.objects.create(name="Chirurgie")
        room_type_radio = RoomType.objects.create(name="Radiologie")

        # Create Rooms
        room1 = Room.objects.create(room_type=room_type_consultation)
        room2 = Room.objects.create(room_type=room_type_surgery)
        room3 = Room.objects.create(room_type=room_type_radio)

        # Create Emergency Types
        emergency_routine = EmergencyType.objects.create(name="Consultation de routine")
        emergency_urgent = EmergencyType.objects.create(name="Urgence")
        emergency_followup = EmergencyType.objects.create(name="Suivi")

        # Create Procedures
        procedure1 = Procedure.objects.create(
            name="Examen clinique complet", price=80.00
        )
        procedure2 = Procedure.objects.create(name="Radiographie", price=150.00)
        procedure3 = Procedure.objects.create(name="Analyse de sang", price=95.00)
        procedure4 = Procedure.objects.create(name="Échographie", price=120.00)

        # Create Equipment
        equipment1 = Equipment.objects.create(name="Stéthoscope")
        equipment2 = Equipment.objects.create(name="Thermomètre")
        equipment3 = Equipment.objects.create(name="Appareil à rayons X")
        equipment4 = Equipment.objects.create(name="Échographe")

        # Create Appointments - one or more per day for next month
        now = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        rooms = [room1, room2, room3]
        emergency_types = [emergency_routine, emergency_urgent, emergency_followup]
        procedures = [procedure1, procedure2, procedure3, procedure4]
        equipment_list = [equipment1, equipment2, equipment3, equipment4]

        appointments = []

        hour_options = [8, 12, 15, 16]
        duration_options = [0.5, 1, 1.5, 2]
        for day in range(30):
            num_appointments = (day % 3) + 1

            for appt_num in range(num_appointments):
                hour = hour_options[appt_num % len(hour_options)]
                duration = duration_options[(day + appt_num) % len(duration_options)]

                appointment = Appointment.objects.create(
                    animal=animals[day % len(animals)],
                    room=rooms[day % len(rooms)],
                    employee=employees[day % len(employees)],
                    emergency_type=emergency_types[day % len(emergency_types)],
                    start_date=now + timedelta(days=day, hours=hour),
                    end_date=now + timedelta(days=day, hours=hour + duration),
                )
                appointments.append(appointment)

                AppointmentProcedure.objects.create(
                    appointment=appointment,
                    procedure=procedures[0],
                    quantity=1,
                )

                AppointmentEquipment.objects.create(
                    appointment=appointment,
                    equipment=equipment_list[0],
                )

                AppointmentItem.objects.create(
                    appointment=appointment,
                    item=items[0],
                    quantity=1,
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {RoomType.objects.count()} room types, "
                f"{Room.objects.count()} rooms, "
                f"{EmergencyType.objects.count()} emergency types, "
                f"{Procedure.objects.count()} procedures, "
                f"{Equipment.objects.count()} equipment items, and "
                f"{Appointment.objects.count()} appointments"
            )
        )
