from django.core.management.base import BaseCommand
from datetime import date
from person.models import Person


class Command(BaseCommand):
    help = 'Populate person data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating person data...")

        # Create Persons
        persons = [
            Person.objects.create(
                first_name="Marie",
                last_name="Dupont",
                phone=41791234567,
                email="marie.dupont@example.ch",
                birthday=date(1985, 3, 15),
                password_hash="hashed_password_1",
            ),
            Person.objects.create(
                first_name="Jean",
                last_name="Martin",
                phone=41791234568,
                email="jean.martin@example.ch",
                birthday=date(1990, 7, 22),
                password_hash="hashed_password_2",
            ),
            Person.objects.create(
                first_name="Sophie",
                last_name="Bernard",
                phone=41791234569,
                email="sophie.bernard@example.ch",
                birthday=date(1988, 11, 5),
                password_hash="hashed_password_3",
            ),
            Person.objects.create(
                first_name="Pierre",
                last_name="Leroy",
                phone=41791234570,
                email="pierre.leroy@example.ch",
                birthday=date(1975, 4, 18),
                password_hash="hashed_password_4",
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
