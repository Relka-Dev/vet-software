from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, date
from decimal import Decimal
from person.models import Person
from employee.models import Role, Employee
from animal.models import Species, Animal
from family.models import Family
from inventory.models import TreatmentType, Item
from .models import (
    RoomType,
    Room,
    EmergencyType,
    Procedure,
    Equipment,
    Appointment,
    AppointmentProcedure,
    AppointmentEquipment,
    AppointmentItem,
)


class RoomTypeModelTest(TestCase):
    """Tests simples pour le modèle RoomType"""

    def test_str_representation(self):
        """Test de la représentation string"""
        room_type = RoomType(name="Consultation")
        self.assertEqual(str(room_type), "Consultation")

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(RoomType._meta.verbose_name, "Type de salle")
        self.assertEqual(RoomType._meta.verbose_name_plural, "Types de salle")


class RoomModelTest(TestCase):
    """Tests simples pour le modèle Room"""

    def setUp(self):
        """Préparation des données de test"""
        self.room_type = RoomType.objects.create(name="Opération")

    def test_str_representation(self):
        """Test de la représentation string"""
        room = Room(room_type=self.room_type)
        self.assertEqual(str(room), "Opération")

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(Room._meta.verbose_name, "Salles")
        self.assertEqual(Room._meta.verbose_name_plural, "Salles")


class EmergencyTypeModelTest(TestCase):
    """Tests simples pour le modèle EmergencyType"""

    def test_str_representation(self):
        """Test de la représentation string"""
        emergency = EmergencyType(name="Urgence vitale")
        self.assertEqual(str(emergency), "Urgence vitale")

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(EmergencyType._meta.verbose_name, "Type de rendez-vous")
        self.assertEqual(
            EmergencyType._meta.verbose_name_plural, "Types de rendez-vous"
        )


class ProcedureModelTest(TestCase):
    """Tests simples pour le modèle Procedure"""

    def test_str_representation(self):
        """Test de la représentation string"""
        procedure = Procedure(name="Vaccination", price=Decimal("50.00"))
        self.assertEqual(str(procedure), "Vaccination - 50.00 CHF")

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(Procedure._meta.verbose_name, "Procédure")
        self.assertEqual(Procedure._meta.verbose_name_plural, "Procédures")

    def test_price_precision(self):
        """Test de la précision du prix"""
        procedure = Procedure(name="Chirurgie", price=Decimal("350.75"))
        self.assertEqual(procedure.price, Decimal("350.75"))


class EquipmentModelTest(TestCase):
    """Tests simples pour le modèle Equipment"""

    def test_str_representation(self):
        """Test de la représentation string"""
        equipment = Equipment(name="Stéthoscope")
        self.assertEqual(str(equipment), "Stéthoscope")

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(Equipment._meta.verbose_name, "Équipement")
        self.assertEqual(Equipment._meta.verbose_name_plural, "Équipements")


class AppointmentModelTest(TestCase):
    """Tests simples pour le modèle Appointment"""

    def setUp(self):
        """Préparation des données de test"""
        # Créer une personne
        person = Person(
            first_name='John',
            last_name='Doe',
            phone=123456789,
            email='john.appointment@example.com',
            birthday=date(1985, 3, 15),
        )
        person.set_password('password')
        person.save()

        # Créer une famille
        self.family = Family.objects.create(main_contact=person)

        # Créer un employé
        role = Role.objects.create(name="Vétérinaire")
        self.employee = Employee.objects.create(
            person=person, first_engagement_date=date(2020, 1, 1), role=role
        )

        # Créer un animal
        species, _ = Species.objects.get_or_create(name="Chien")
        self.animal = Animal.objects.create(
            name="Rex", species=species, family=self.family, birthday=date(2020, 5, 10)
        )

        # Créer une salle
        room_type = RoomType.objects.create(name="Consultation")
        self.room = Room.objects.create(room_type=room_type)

        # Créer un type d'urgence
        self.emergency_type = EmergencyType.objects.create(name="Routine")

    def test_str_representation(self):
        """Test de la représentation string"""
        appointment = Appointment(
            animal=self.animal,
            room=self.room,
            employee=self.employee,
            emergency_type=self.emergency_type,
            start_date=timezone.make_aware(datetime(2025, 6, 15, 10, 0)),
            end_date=timezone.make_aware(datetime(2025, 6, 15, 11, 0)),
        )
        result = str(appointment)
        self.assertIn("Rex", result)
        self.assertIn("Consultation", result)
        self.assertIn("Routine", result)

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(Appointment._meta.verbose_name, "Consultation")
        self.assertEqual(Appointment._meta.verbose_name_plural, "Consultations")

    def test_clean_no_conflict(self):
        """Test que clean ne lève pas en cas de rdv unique"""
        appointment = Appointment(
            animal=self.animal,
            room=self.room,
            employee=self.employee,
            emergency_type=self.emergency_type,
            start_date=timezone.make_aware(datetime(2025, 6, 15, 10, 0)),
            end_date=timezone.make_aware(datetime(2025, 6, 15, 11, 0)),
        )
        # Ne devrait pas lever d'exception
        appointment.clean()

    def test_clean_with_conflict(self):
        """Test que clean détecte les conflits de rendez-vous"""
        # Créer un premier rendez-vous
        appointment1 = Appointment.objects.create(
            animal=self.animal,
            room=self.room,
            employee=self.employee,
            emergency_type=self.emergency_type,
            start_date=timezone.make_aware(datetime(2025, 6, 15, 10, 0)),
            end_date=timezone.make_aware(datetime(2025, 6, 15, 11, 0)),
        )

        # Créer un rendez-vous qui chevauche
        appointment2 = Appointment(
            animal=self.animal,
            room=self.room,
            employee=self.employee,
            emergency_type=self.emergency_type,
            start_date=timezone.make_aware(datetime(2025, 6, 15, 10, 30)),
            end_date=timezone.make_aware(datetime(2025, 6, 15, 11, 30)),
        )

        # Devrait lever une ValidationError
        with self.assertRaises(ValidationError):
            appointment2.clean()

    def test_clean_with_nearmiss(self):
        """Test que clean ne fait pas d'erreur si le rendez vous est juste après un autre"""
        # Créer un premier rendez-vous
        appointment1 = Appointment.objects.create(
            animal=self.animal,
            room=self.room,
            employee=self.employee,
            emergency_type=self.emergency_type,
            start_date=timezone.make_aware(datetime(2025, 6, 15, 10, 0)),
            end_date=timezone.make_aware(datetime(2025, 6, 15, 11, 0)),
        )

        appointment2 = Appointment(
            animal=self.animal,
            room=self.room,
            employee=self.employee,
            emergency_type=self.emergency_type,
            start_date=timezone.make_aware(datetime(2025, 6, 15, 11, 00)),
            end_date=timezone.make_aware(datetime(2025, 6, 15, 11, 30)),
        )

        appointment3 = Appointment(
            animal=self.animal,
            room=self.room,
            employee=self.employee,
            emergency_type=self.emergency_type,
            start_date=timezone.make_aware(datetime(2025, 6, 15, 9, 00)),
            end_date=timezone.make_aware(datetime(2025, 6, 15, 10, 00)),
        )

        # Devrait pas lever une ValidationError
        appointment2.clean()
        appointment3.clean()


class AppointmentProcedureModelTest(TestCase):
    """Tests simples pour le modèle AppointmentProcedure"""

    def setUp(self):
        """Préparation des données de test"""
        # Setup minimal pour créer un appointment
        person = Person(
            first_name='Jane',
            last_name='Smith',
            phone=987654321,
            email='jane.procedure@example.com',
            birthday=date(1990, 7, 20),
        )
        person.set_password('password')
        person.save()

        family = Family.objects.create(main_contact=person)
        role = Role.objects.create(name="Assistant")
        employee = Employee.objects.create(
            person=person, first_engagement_date=date(2021, 1, 1), role=role
        )

        species, _ = Species.objects.get_or_create(name="Chat")
        animal = Animal.objects.create(
            name="Minou", species=species, family=family, birthday=date(2019, 3, 5)
        )

        room_type = RoomType.objects.create(name="Radio")
        room = Room.objects.create(room_type=room_type)
        emergency_type = EmergencyType.objects.create(name="Contrôle")

        self.appointment = Appointment.objects.create(
            animal=animal,
            room=room,
            employee=employee,
            emergency_type=emergency_type,
            start_date=timezone.make_aware(datetime(2025, 7, 1, 14, 0)),
            end_date=timezone.make_aware(datetime(2025, 7, 1, 15, 0)),
        )

        self.procedure = Procedure.objects.create(
            name="Radiographie", price=Decimal("120.00")
        )

    def test_str_representation(self):
        """Test de la représentation string"""
        app_procedure = AppointmentProcedure(
            appointment=self.appointment, procedure=self.procedure, quantity=2
        )
        result = str(app_procedure)
        self.assertIn("Quantity : 2", result)

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(
            AppointmentProcedure._meta.verbose_name,
            "Association consultation/procédure",
        )
        self.assertEqual(
            AppointmentProcedure._meta.verbose_name_plural,
            "Associations consultation/procédure",
        )


class AppointmentEquipmentModelTest(TestCase):
    """Tests simples pour le modèle AppointmentEquipment"""

    def setUp(self):
        """Préparation des données de test"""
        person = Person(
            first_name='Bob',
            last_name='Wilson',
            phone=555000111,
            email='bob.equipment@example.com',
            birthday=date(1982, 11, 12),
        )
        person.set_password('password')
        person.save()

        family = Family.objects.create(main_contact=person)
        role = Role.objects.create(name="Technicien")
        employee = Employee.objects.create(
            person=person, first_engagement_date=date(2019, 6, 1), role=role
        )

        species, _ = Species.objects.get_or_create(name="Lapin")
        animal = Animal.objects.create(
            name="Fluffy", species=species, family=family, birthday=date(2022, 1, 15)
        )

        room_type = RoomType.objects.create(name="Examen")
        room = Room.objects.create(room_type=room_type)
        emergency_type = EmergencyType.objects.create(name="Urgence")

        self.appointment = Appointment.objects.create(
            animal=animal,
            room=room,
            employee=employee,
            emergency_type=emergency_type,
            start_date=timezone.make_aware(datetime(2025, 8, 10, 9, 0)),
            end_date=timezone.make_aware(datetime(2025, 8, 10, 10, 0)),
        )

        self.equipment = Equipment.objects.create(name="Échographe")

    def test_str_representation(self):
        """Test de la représentation string"""
        app_equipment = AppointmentEquipment(
            appointment=self.appointment, equipment=self.equipment
        )
        result = str(app_equipment)
        self.assertIn("Échographe", result)

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(
            AppointmentEquipment._meta.verbose_name,
            "Association consultation/équipement",
        )
        self.assertEqual(
            AppointmentEquipment._meta.verbose_name_plural,
            "Associations consultation/équipement",
        )


class AppointmentItemModelTest(TestCase):
    """Tests simples pour le modèle AppointmentItem"""

    def setUp(self):
        """Préparation des données de test"""
        person = Person(
            first_name='Alice',
            last_name='Brown',
            phone=777888999,
            email='alice.item@example.com',
            birthday=date(1995, 4, 25),
        )
        person.set_password('password')
        person.save()

        family = Family.objects.create(main_contact=person)
        role = Role.objects.create(name="Chirurgien")
        employee = Employee.objects.create(
            person=person, first_engagement_date=date(2018, 3, 15), role=role
        )

        species, _ = Species.objects.get_or_create(name="Oiseau")
        animal = Animal.objects.create(
            name="Tweety", species=species, family=family, birthday=date(2023, 6, 1)
        )

        room_type = RoomType.objects.create(name="Chirurgie")
        room = Room.objects.create(room_type=room_type)
        emergency_type = EmergencyType.objects.create(name="Intervention")

        self.appointment = Appointment.objects.create(
            animal=animal,
            room=room,
            employee=employee,
            emergency_type=emergency_type,
            start_date=timezone.make_aware(datetime(2025, 9, 5, 13, 0)),
            end_date=timezone.make_aware(datetime(2025, 9, 5, 15, 0)),
        )

        treatment_type = TreatmentType.objects.create(type="Anesthésie")
        self.item = Item.objects.create(
            treatment_type=treatment_type, name="Anesthésiant", price=Decimal("80.00")
        )

    def test_str_representation(self):
        """Test de la représentation string"""
        app_item = AppointmentItem(
            appointment=self.appointment, item=self.item, quantity=3
        )
        result = str(app_item)
        self.assertIn("3", result)

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(
            AppointmentItem._meta.verbose_name, "Association consultation/article"
        )
        self.assertEqual(
            AppointmentItem._meta.verbose_name_plural,
            "Associations consultation/article",
        )
