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

        # Create Appointments
        now = timezone.now()

        appointment1 = Appointment.objects.create(
            animal=animals[0],
            room=room1,
            employee=employees[0],
            emergency_type=emergency_routine,
            start_date=now + timedelta(days=3, hours=9),
            end_date=now + timedelta(days=3, hours=10),
        )
        appointment2 = Appointment.objects.create(
            animal=animals[1],
            room=room3,
            employee=employees[1],
            emergency_type=emergency_urgent,
            start_date=now + timedelta(days=4, hours=14),
            end_date=now + timedelta(days=4, hours=15),
        )
        appointment3 = Appointment.objects.create(
            animal=animals[2],
            room=room1,
            employee=employees[0],
            emergency_type=emergency_followup,
            start_date=now + timedelta(days=5, hours=11),
            end_date=now + timedelta(days=5, hours=11, minutes=30),
        )
        appointment4 = Appointment.objects.create(
            animal=animals[0],
            room=room2,
            employee=employees[1],
            emergency_type=emergency_urgent,
            start_date=now + timedelta(days=7, hours=10),
            end_date=now + timedelta(days=7, hours=12),
        )

        # Link Appointments with Procedures
        AppointmentProcedure.objects.create(
            appointment=appointment1, procedure=procedure1, quantity=1
        )
        AppointmentProcedure.objects.create(
            appointment=appointment2, procedure=procedure2, quantity=1
        )
        AppointmentProcedure.objects.create(
            appointment=appointment2, procedure=procedure3, quantity=1
        )
        AppointmentProcedure.objects.create(
            appointment=appointment3, procedure=procedure1, quantity=1
        )
        AppointmentProcedure.objects.create(
            appointment=appointment4, procedure=procedure4, quantity=1
        )

        # Link Appointments with Equipment
        AppointmentEquipment.objects.create(
            appointment=appointment1, equipment=equipment1
        )
        AppointmentEquipment.objects.create(
            appointment=appointment1, equipment=equipment2
        )
        AppointmentEquipment.objects.create(
            appointment=appointment2, equipment=equipment3
        )
        AppointmentEquipment.objects.create(
            appointment=appointment3, equipment=equipment1
        )
        AppointmentEquipment.objects.create(
            appointment=appointment4, equipment=equipment4
        )

        # Link Appointments with Items
        AppointmentItem.objects.create(
            appointment=appointment1, item=items[0], quantity=1
        )
        AppointmentItem.objects.create(
            appointment=appointment2, item=items[1], quantity=2
        )
        AppointmentItem.objects.create(
            appointment=appointment3, item=items[0], quantity=1
        )
        AppointmentItem.objects.create(
            appointment=appointment4, item=items[2], quantity=1
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
