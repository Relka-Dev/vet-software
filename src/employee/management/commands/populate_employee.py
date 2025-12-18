from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from person.models import Person
from employee.models import Role, Employee, AvailabilityRange, AvailabilityEmployee


class Command(BaseCommand):
    help = 'Populate employee data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating employee data...")

        persons = list(Person.objects.all())
        if len(persons) < 3:
            self.stdout.write(
                self.style.ERROR("Not enough persons. Run populate_person.")
            )
            return

        # Create Roles
        role_vet = Role.objects.create(name="Vétérinaire")
        role_receptionist = Role.objects.create(name="Réceptionniste")
        role_student = Role.objects.create(name="Étudiant vétérinaire")

        # Create Employees
        employee_vet1 = Employee.objects.create(
            person=persons[0],
            first_engagement_date=date(2015, 1, 10),
            role=role_vet,
        )
        employee_vet2 = Employee.objects.create(
            person=persons[1],
            first_engagement_date=date(2018, 6, 15),
            role=role_vet,
        )
        employee_receptionist = Employee.objects.create(
            person=persons[2],
            first_engagement_date=date(2020, 3, 1),
            role=role_receptionist,
        )

        # Create Availability Ranges
        now = timezone.now()
        availability1 = AvailabilityRange.objects.create(
            start_date=now + timedelta(days=1, hours=8),
            end_date=now + timedelta(days=1, hours=12),
        )
        availability2 = AvailabilityRange.objects.create(
            start_date=now + timedelta(days=1, hours=14),
            end_date=now + timedelta(days=1, hours=18),
        )
        availability3 = AvailabilityRange.objects.create(
            start_date=now + timedelta(days=2, hours=8),
            end_date=now + timedelta(days=2, hours=17),
        )
        availability4 = AvailabilityRange.objects.create(
            start_date=now + timedelta(days=3, hours=9),
            end_date=now + timedelta(days=3, hours=16),
        )

        # Link employees to availability
        AvailabilityEmployee.objects.create(
            employee=employee_vet1, availability_range=availability1
        )
        AvailabilityEmployee.objects.create(
            employee=employee_vet1, availability_range=availability2
        )
        AvailabilityEmployee.objects.create(
            employee=employee_vet2, availability_range=availability3
        )
        AvailabilityEmployee.objects.create(
            employee=employee_receptionist, availability_range=availability4
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {Role.objects.count()} roles, "
                f"{Employee.objects.count()} employees, and "
                f"{AvailabilityRange.objects.count()} availability ranges"
            )
        )
