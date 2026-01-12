from django.test import TestCase
from django.utils import timezone
from datetime import date
from person.models import Person
from family.models import Family
from employee.models import Role, Employee
from .models import Species, Animal, SOAPNote


class SpeciesModelTest(TestCase):
    """Tests simples pour le modèle Species"""

    def test_str_representation(self):
        """Test de la représentation string"""
        species = Species(name="Chien")
        self.assertEqual(str(species), "Chien")

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(Species._meta.verbose_name, "Espèce")
        self.assertEqual(Species._meta.verbose_name_plural, "Espèces")

    def test_name_uniqueness(self):
        """Test que name doit être unique"""
        Species.objects.create(name="Chat")
        
        # Tenter de créer une autre espèce avec le même nom
        with self.assertRaises(Exception):
            Species.objects.create(name="Chat")


class AnimalModelTest(TestCase):
    """Tests simples pour le modèle Animal"""

    def setUp(self):
        """Préparation des données de test"""
        person = Person(
            first_name='John',
            last_name='Doe',
            phone=123456789,
            email='john.animal@example.com',
            birthday=date(1985, 3, 15)
        )
        person.set_password('password')
        person.save()

        self.family = Family.objects.create(main_contact=person)
        self.species, _ = Species.objects.get_or_create(name="Chien")

    def test_str_representation(self):
        """Test de la représentation string"""
        animal = Animal(
            name="Rex",
            species=self.species,
            family=self.family,
            birthday=date(2020, 5, 10),
            federal_identification="CH123456"
        )
        result = str(animal)
        self.assertIn("Rex", result)
        self.assertIn("Chien", result)
        self.assertIn("Doe", result)
        self.assertIn("2020-05-10", result)

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(Animal._meta.verbose_name, "Animal")
        self.assertEqual(Animal._meta.verbose_name_plural, "Animaux")

    def test_animal_with_death_date(self):
        """Test qu'un animal peut avoir une date de décès"""
        animal = Animal.objects.create(
            name="Buddy",
            species=self.species,
            family=self.family,
            birthday=date(2010, 3, 5),
            death_date=date(2023, 12, 25),
            federal_identification="CH456789"
        )
        self.assertEqual(animal.death_date, date(2023, 12, 25))


class SOAPNoteModelTest(TestCase):
    """Tests simples pour le modèle SOAPNote"""

    def setUp(self):
        """Préparation des données de test"""
        person = Person(
            first_name='Jane',
            last_name='Smith',
            phone=987654321,
            email='jane.soap@example.com',
            birthday=date(1990, 7, 20)
        )
        person.set_password('password')
        person.save()

        family = Family.objects.create(main_contact=person)
        species, _ = Species.objects.get_or_create(name="Chat")
        
        self.animal = Animal.objects.create(
            name="Minou",
            species=species,
            family=family,
            birthday=date(2019, 3, 5),
            federal_identification="CH111222"
        )

        role = Role.objects.create(name="Vétérinaire")
        self.employee = Employee.objects.create(
            person=person,
            first_engagement_date=date(2020, 1, 1),
            role=role
        )

    def test_str_representation(self):
        """Test de la représentation string"""
        note = SOAPNote(
            content="Note de consultation",
            animal=self.animal,
            text_subjective="Le chat tousse",
            text_objective="Température normale",
            text_assessment="Infection respiratoire légère",
            text_plan="Antibiotiques pendant 7 jours",
            created_by=self.employee
        )
        result = str(note)
        self.assertIn("Note de consultation", result)
        self.assertIn("Minou", result)

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(SOAPNote._meta.verbose_name, "SOAP Note")
        self.assertEqual(SOAPNote._meta.verbose_name_plural, "SOAP Notes")

    def test_created_at_auto(self):
        """Test que created_at est automatique"""
        note = SOAPNote.objects.create(
            content="Consultation de routine",
            animal=self.animal,
            text_subjective="Aucun symptôme",
            text_objective="État général bon",
            text_assessment="Animal en bonne santé",
            text_plan="Prochain contrôle dans 6 mois",
            created_by=self.employee
        )
        self.assertIsNotNone(note.created_at)

    def test_note_with_validator(self):
        """Test qu'une note peut avoir un validateur"""
        # Créer un deuxième employé pour la validation
        person2 = Person(
            first_name='Bob',
            last_name='Wilson',
            phone=555000111,
            email='bob.validator@example.com',
            birthday=date(1982, 11, 12)
        )
        person2.set_password('password')
        person2.save()

        role2 = Role.objects.create(name="Vétérinaire Senior")
        validator = Employee.objects.create(
            person=person2,
            first_engagement_date=date(2015, 1, 1),
            role=role2
        )

        note = SOAPNote.objects.create(
            content="Note validée",
            animal=self.animal,
            text_subjective="Examen complet",
            text_objective="Tous les paramètres normaux",
            text_assessment="Animal en excellente santé",
            text_plan="Vaccination annuelle",
            created_by=self.employee,
            validated_by=validator
        )
        self.assertEqual(note.validated_by, validator)

    def test_soap_fields_required(self):
        """Test que les champs SOAP sont tous présents"""
        note = SOAPNote(
            content="Test SOAP",
            animal=self.animal,
            text_subjective="S",
            text_objective="O",
            text_assessment="A",
            text_plan="P",
            created_by=self.employee
        )
        self.assertEqual(note.text_subjective, "S")
        self.assertEqual(note.text_objective, "O")
        self.assertEqual(note.text_assessment, "A")
        self.assertEqual(note.text_plan, "P")