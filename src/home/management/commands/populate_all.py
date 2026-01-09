from django.core.management.base import BaseCommand
from django.core.management import call_command

from appointment.models import (
    AppointmentEquipment,
    AppointmentProcedure,
    AppointmentItem,
    Appointment,
    Equipment,
    Procedure,
    EmergencyType,
    Room,
    RoomType,
)
from inventory.models import Inventory, Item, TreatmentType
from animal.models import SOAPNote, Animal
from employee.models import AvailabilityEmployee, Employee, OpenHours, Role
from family.models import Extra_family_member, Family
from person.models import Person


class Command(BaseCommand):
    help = 'Populate all database tables with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.WARNING("Starting complete database population...")
        )

        self.stdout.write("\nClearing existing data...")
        AppointmentItem.objects.all().delete()
        AppointmentEquipment.objects.all().delete()
        AppointmentProcedure.objects.all().delete()
        Appointment.objects.all().delete()
        Equipment.objects.all().delete()
        Procedure.objects.all().delete()
        EmergencyType.objects.all().delete()
        Room.objects.all().delete()
        RoomType.objects.all().delete()
        Inventory.objects.all().delete()
        Item.objects.all().delete()
        TreatmentType.objects.all().delete()
        SOAPNote.objects.all().delete()
        Animal.objects.all().delete()
        AvailabilityEmployee.objects.all().delete()
        Employee.objects.all().delete()
        Role.objects.all().delete()
        Extra_family_member.objects.all().delete()
        Family.objects.all().delete()
        Person.objects.all().delete()
        OpenHours.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("All existing data cleared"))

        commands = [
            'populate_person',
            'populate_family',
            'populate_employee',
            'populate_animal',
            'populate_inventory',
            'populate_appointment',
            'populate_open_hours',
        ]

        for command in commands:
            call_command(command)

        self.stdout.write(self.style.SUCCESS("✓ All data successfully populated!"))
