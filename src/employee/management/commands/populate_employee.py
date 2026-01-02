from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta, time
from person.models import Person
from employee.models import Role, Employee, AvailabilityEmployee


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

        # Create Availability for employees
        AvailabilityEmployee.objects.create(
            employee=employee_vet1,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            day_of_week=0,  # Monday
            start_time=time(8, 0),
            end_time=time(12, 0),
        )
        AvailabilityEmployee.objects.create(
            employee=employee_vet1,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            day_of_week=0,
            start_time=time(14, 0),
            end_time=time(18, 0),
        )
        AvailabilityEmployee.objects.create(
            employee=employee_vet1,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            day_of_week=1,
            start_time=time(8, 0),
            end_time=time(12, 0),
        )
        AvailabilityEmployee.objects.create(
            employee=employee_vet1,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            day_of_week=1,
            start_time=time(14, 0),
            end_time=time(18, 0),
        )
        AvailabilityEmployee.objects.create(
            employee=employee_vet1,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            day_of_week=2,
            start_time=time(8, 0),
            end_time=time(12, 0),
        )
        AvailabilityEmployee.objects.create(
            employee=employee_vet1,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            day_of_week=2,
            start_time=time(14, 0),
            end_time=time(18, 0),
        )
        AvailabilityEmployee.objects.create(
            employee=employee_vet1,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            day_of_week=3,
            start_time=time(8, 0),
            end_time=time(12, 0),
        )
        AvailabilityEmployee.objects.create(
            employee=employee_vet1,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            day_of_week=3,
            start_time=time(14, 0),
            end_time=time(18, 0),
        )
        AvailabilityEmployee.objects.create(
            employee=employee_vet1,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            day_of_week=4,
            start_time=time(8, 0),
            end_time=time(12, 0),
        )
        AvailabilityEmployee.objects.create(
            employee=employee_vet1,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            day_of_week=4,
            start_time=time(14, 0),
            end_time=time(18, 0),
        )

        # Employee 2:
        for day in [0, 2, 4]:  # Monday, Wednesday, Friday
            AvailabilityEmployee.objects.create(
                employee=employee_vet2,
                start_date=date(2025, 1, 1),
                end_date=date(2025, 12, 31),
                day_of_week=day,
                start_time=time(9, 0),
                end_time=time(17, 0),
            )

        # Receptionist: Lundi-Vendredi, 8h-17h
        for day in range(5):
            AvailabilityEmployee.objects.create(
                employee=employee_receptionist,
                start_date=date(2025, 1, 1),
                end_date=date(2025, 12, 31),
                day_of_week=day,
                start_time=time(8, 0),
                end_time=time(17, 0),
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {Role.objects.count()} roles, "
                f"{Employee.objects.count()} employees, and "
                f"{AvailabilityEmployee.objects.count()} availability schedules"
            )
        )
