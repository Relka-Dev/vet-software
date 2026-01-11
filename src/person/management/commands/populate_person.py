from django.core.management.base import BaseCommand
from datetime import date
from person.models import Person
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Populate person data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating person data...")

        # Create Persons
        persons = [
            Person.objects.create(
                first_name="Grace",
                last_name="Naing",
                phone=41791234567,
                email="grace.naing@vet.ch",
                birthday=date(1985, 3, 15),
                password_hash=make_password("1234"),
            ),
            Person.objects.create(
                first_name="Karel",
                last_name="Svoboda",
                phone=41791234568,
                email="karel.svoboda@vet.ch",
                birthday=date(1990, 7, 22),
                password_hash=make_password("1234"),
            ),
            Person.objects.create(
                first_name="Aurélie",
                last_name="Pham",
                phone=41791234569,
                email="aurelie.pham@vet.ch",
                birthday=date(1988, 11, 5),
                password_hash=make_password("1234"),
            ),
            Person.objects.create(
                first_name="Martin",
                last_name="Martin",
                phone=41791234570,
                email="martin.martin@vet.ch",
                birthday=date(1975, 4, 18),
                password_hash=make_password("1234"),
            ),
            Person.objects.create(
                first_name="Claire",
                last_name="Moreau",
                phone=41791234571,
                email="claire.moreau@example.ch",
                birthday=date(1992, 9, 30),
                password_hash="hashed_password_5",
            ),
            Person.objects.create(
                first_name="Thomas",
                last_name="Petit",
                phone=41791234572,
                email="thomas.petit@example.ch",
                birthday=date(1983, 12, 8),
                password_hash="hashed_password_6",
            ),
        ]

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {len(persons)} persons")
        )
