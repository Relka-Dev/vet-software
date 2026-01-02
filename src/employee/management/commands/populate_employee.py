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
        availability_schedules = [
            (
                employee_vet1,
                range(5),
                [(8, 0, 12, 0), (14, 0, 18, 0)],
                [(2025, 2025), (2026, 2026)],
            ),
            (employee_vet2, [0, 2, 4], [(9, 0, 17, 0)], [(2025, 2026)]),
            (employee_receptionist, range(5), [(8, 0, 17, 0)], [(2025, 2026)]),
        ]

        for employee, days, slots, year_ranges in availability_schedules:
            for year_start, year_end in year_ranges:
                for day in days:
                    for start_h, start_m, end_h, end_m in slots:
                        AvailabilityEmployee.objects.create(
                            employee=employee,
                            start_date=date(year_start, 1, 1),
                            end_date=date(year_end, 12, 31),
                            day_of_week=day,
                            start_time=time(start_h, start_m),
                            end_time=time(end_h, end_m),
                        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {Role.objects.count()} roles, "
                f"{Employee.objects.count()} employees, and "
                f"{AvailabilityEmployee.objects.count()} availability schedules"
            )
        )
