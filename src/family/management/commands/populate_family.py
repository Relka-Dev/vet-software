from django.core.management.base import BaseCommand
from datetime import date
from person.models import Person
from family.models import Family, Extra_family_member


class Command(BaseCommand):
    help = 'Populate family data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating family data...")

        persons = list(Person.objects.all())
        if len(persons) < 6:
            self.stdout.write(
                self.style.ERROR("Not enough persons. Run populate_person.")
            )
            return

        # Create Families
        family1 = Family.objects.create(
            main_contact=persons[3], creation_date=date(2020, 5, 12)
        )
        family2 = Family.objects.create(
            main_contact=persons[4], creation_date=date(2021, 8, 20)
        )
        family3 = Family.objects.create(
            main_contact=persons[5], creation_date=date(2019, 3, 5)
        )

        # Create extra family members
        Extra_family_member.objects.create(family=family1, person=persons[0])
        Extra_family_member.objects.create(family=family2, person=persons[1])

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {Family.objects.count()} families and "
                f"{Extra_family_member.objects.count()} extra members"
            )
        )
