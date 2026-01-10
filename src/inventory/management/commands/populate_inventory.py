from django.core.management.base import BaseCommand
from datetime import date
from inventory.models import TreatmentType, Item, Inventory


class Command(BaseCommand):
    help = 'Populate inventory data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating inventory data...")

        # Create Treatment Types
        treatment_vaccination = TreatmentType.objects.create(type="Vaccination")
        treatment_consultation = TreatmentType.objects.create(type="Consultation")
        treatment_surgery = TreatmentType.objects.create(type="Chirurgie")
        treatment_emergency = TreatmentType.objects.create(type="Urgence")

        # Create Items
        item1 = Item.objects.create(
            treatment_type=treatment_vaccination,
            name="Vaccin antirabique",
            reminder=True,
            price=45.00,
        )
        item2 = Item.objects.create(
            treatment_type=treatment_vaccination,
            name="Vaccin combiné (DHPP)",
            reminder=True,
            price=55.00,
        )
        item3 = Item.objects.create(
            treatment_type=treatment_consultation,
            name="Antibiotique (comprimés)",
            reminder=False,
            price=25.50,
        )
        item4 = Item.objects.create(
            treatment_type=treatment_consultation,
            name="Anti-inflammatoire",
            reminder=False,
            price=18.75,
        )
        item5 = Item.objects.create(
            treatment_type=treatment_surgery,
            name="Anesthésique",
            reminder=False,
            price=120.00,
        )
        item6 = Item.objects.create(
            treatment_type=treatment_surgery,
            name="Kit de suture",
            reminder=False,
            price=35.00,
        )
        item7 = Item.objects.create(
            treatment_type=treatment_emergency,
            name="Sérum physiologique",
            reminder=False,
            price=12.00,
        )

        # Create Inventory
        Inventory.objects.create(
            item=item1,
            quantity=1200,
            expiration_date=date(2026, 12, 31),
        )
        Inventory.objects.create(
            item=item2,
            quantity=3000,
            expiration_date=date(2026, 8, 15),
        )
        Inventory.objects.create(
            item=item3,
            quantity=1000,
            expiration_date=date(2025, 6, 30),
        )
        Inventory.objects.create(
            item=item4,
            quantity=2500,
            expiration_date=date(2026, 3, 20),
        )
        Inventory.objects.create(
            item=item5,
            quantity=2000,
            expiration_date=date(2027, 3, 15),
        )
        Inventory.objects.create(
            item=item6,
            quantity=600,
            expiration_date=date(2028, 1, 10),
        )
        Inventory.objects.create(
            item=item7,
            quantity=2000,
            expiration_date=date(2026, 9, 30),
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {TreatmentType.objects.count()} treatment types, "
                f"{Item.objects.count()} items, and "
                f"{Inventory.objects.count()} inventory entries"
            )
        )
