from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from family.models import Family
from animal.models import Animal, SOAPNote
from employee.models import Employee


class Command(BaseCommand):
    help = 'Populate animal data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating animal data...")

        families = list(Family.objects.all())
        if len(families) < 2:
            self.stdout.write(
                self.style.ERROR("Not enough families. Run populate_family first.")
            )
            return

        employees = list(Employee.objects.filter(role__name="Vétérinaire"))
        if len(employees) < 2:
            self.stdout.write(
                self.style.ERROR(
                    "Not enough veterinarians. Run populate_employee first."
                )
            )
            return

        # Animal data
        animal1 = Animal.objects.create(
            name="Max",
            birthday=date(2018, 3, 10),
            federal_identification="CH-123-456-789",
            family=families[0],
        )
        animal2 = Animal.objects.create(
            name="Luna",
            birthday=date(2019, 7, 15),
            federal_identification="CH-987-654-321",
            family=families[0],
        )
        animal3 = Animal.objects.create(
            name="Charlie",
            birthday=date(2020, 1, 5),
            federal_identification="CH-555-666-777",
            family=families[1],
        )
        animal4 = Animal.objects.create(
            name="Bella",
            birthday=date(2017, 11, 20),
            federal_identification="CH-111-222-333",
            family=families[1],
        )

        # SOAP Notes
        SOAPNote.objects.create(
            content="Détartrage et nettoyage",
            created_at=timezone.now() - timedelta(days=9),
            animal=animal1,
            text_subjective="Animal en bonne santé",
            text_objective="Température normale, poids stable à 15kg",
            text_assessment="Aucun problème détecté",
            text_plan="Détartrage et nettoyage effectués. Prochain contrôle dans a 1an.",
            created_by=employees[1],
            validated_by=employees[1],
        )
        SOAPNote.objects.create(
            content="Vaccination annuelle",
            created_at=timezone.now() - timedelta(days=10),
            animal=animal1,
            text_subjective="Animal en bonne santé",
            text_objective="Température normale, poids stable à 15kg",
            text_assessment="Aucun problème détecté",
            text_plan="Vaccination antirabique effectuée. Prochain rappel dans 1 an.",
            created_by=employees[0],
            validated_by=employees[0],
        )
        SOAPNote.objects.create(
            content="Consultation dermatologie",
            created_at=timezone.now() - timedelta(days=5),
            animal=animal2,
            text_subjective="Démangeaisons fréquentes depuis 2 semaines",
            text_objective="Rougeurs sur l'abdomen et entre les pattes",
            text_assessment="Possible allergie alimentaire ou parasites",
            text_plan="Changement de régime alimentaire. Revoir dans 2 semaines.",
            created_by=employees[1],
            validated_by=employees[0],
        )
        SOAPNote.objects.create(
            content="Contrôle de routine",
            created_at=timezone.now() - timedelta(days=15),
            animal=animal3,
            text_subjective="Jeune chat actif, pas de plaintes",
            text_objective="Bon état général, dentition saine",
            text_assessment="Animal en excellente santé",
            text_plan="Rappel vaccination dans 6 mois",
            created_by=employees[0],
            validated_by=employees[0],
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {Animal.objects.count()} animals and "
                f"{SOAPNote.objects.count()} SOAP notes"
            )
        )
