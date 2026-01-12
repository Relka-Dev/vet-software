from django.test import TestCase
from datetime import date, time, datetime
from person.models import Person
from .models import (
    Role, Employee, OpenHours, OpenException,
    AvailabilityEmployee, AvailabilityException
)


class RoleModelTest(TestCase):
    """Tests simples pour le modèle Role"""

    def test_str_representation(self):
        """Test de la représentation string"""
        role = Role(name="Vétérinaire")
        self.assertEqual(str(role), "Vétérinaire")

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(Role._meta.verbose_name, "Fonction de l'employé(e)")
        self.assertEqual(Role._meta.verbose_name_plural, "Fonctions de l'employé(e)")


class EmployeeModelTest(TestCase):
    """Tests simples pour le modèle Employee"""

    def setUp(self):
        """Préparation des données de test"""
        self.person = Person(
            first_name='John',
            last_name='Doe',
            phone=123456789,
            email='john.employee@example.com',
            birthday=date(1985, 3, 15)
        )
        self.person.set_password('password')
        self.person.save()

        self.role = Role.objects.create(name="Réceptionniste")

    def test_str_representation(self):
        """Test de la représentation string"""
        employee = Employee(
            person=self.person,
            first_engagement_date=date(2020, 1, 15),
            role=self.role
        )
        expected = f"{self.person} - 2020-01-15 - {self.role}"
        self.assertEqual(str(employee), expected)

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(Employee._meta.verbose_name, "Employé(e)")
        self.assertEqual(Employee._meta.verbose_name_plural, "Employé(e)s")


class OpenHoursModelTest(TestCase):
    """Tests simples pour le modèle OpenHours"""

    def test_str_representation(self):
        """Test de la représentation string"""
        open_hours = OpenHours(
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            day_of_week=0,  # Lundi
            start_time=time(8, 0),
            end_time=time(18, 0)
        )
        expected = "Lundi : 08:00:00 - 18:00:00 (2025-01-01 to 2025-12-31)"
        self.assertEqual(str(open_hours), expected)

    def test_get_day_of_week_display(self):
        """Test de l'affichage du jour de la semaine"""
        open_hours = OpenHours(
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            day_of_week=3,  # Jeudi
            start_time=time(9, 0),
            end_time=time(17, 0)
        )
        self.assertEqual(open_hours.get_day_of_week_display(), "Jeudi")

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(OpenHours._meta.verbose_name, "Heure d'ouverture")
        self.assertEqual(OpenHours._meta.verbose_name_plural, "Heures d'ouverture")

    def test_days_of_week_choices(self):
        """Test que tous les jours de la semaine sont disponibles"""
        days = dict(OpenHours.DAYS_OF_WEEK)
        self.assertEqual(days[0], "Lundi")
        self.assertEqual(days[6], "Dimanche")
        self.assertEqual(len(days), 7)


class OpenExceptionModelTest(TestCase):
    """Tests simples pour le modèle OpenException"""

    def test_str_representation_open(self):
        """Test de la représentation string quand ouvert"""
        exception = OpenException(
            start_date=datetime(2025, 12, 25, 10, 0),
            end_date=datetime(2025, 12, 25, 14, 0),
            is_open=True
        )
        self.assertIn("Ouvert", str(exception))

    def test_str_representation_closed(self):
        """Test de la représentation string quand fermé"""
        exception = OpenException(
            start_date=datetime(2025, 12, 24, 0, 0),
            end_date=datetime(2025, 12, 24, 23, 59),
            is_open=False
        )
        self.assertIn("Fermé", str(exception))

    def test_is_open_default_value(self):
        """Test que is_open est False par défaut"""
        exception = OpenException(
            start_date=datetime(2025, 1, 1, 0, 0),
            end_date=datetime(2025, 1, 1, 23, 59)
        )
        self.assertFalse(exception.is_open)

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(OpenException._meta.verbose_name, "Exception aux heures d'ouverture")
        self.assertEqual(OpenException._meta.verbose_name_plural, "Exceptions aux heures d'ouverture")


class AvailabilityEmployeeModelTest(TestCase):
    """Tests simples pour le modèle AvailabilityEmployee"""

    def setUp(self):
        """Préparation des données de test"""
        person = Person(
            first_name='Jane',
            last_name='Smith',
            phone=987654321,
            email='jane.smith@example.com',
            birthday=date(1990, 6, 20)
        )
        person.set_password('password')
        person.save()

        role = Role.objects.create(name="Vétérinaire")

        self.employee = Employee.objects.create(
            person=person,
            first_engagement_date=date(2021, 5, 1),
            role=role
        )

    def test_str_representation(self):
        """Test de la représentation string"""
        availability = AvailabilityEmployee(
            employee=self.employee,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            day_of_week=2,  # Mercredi
            start_time=time(9, 0),
            end_time=time(17, 0)
        )
        self.assertIn("Mercredi", str(availability))
        self.assertIn("09:00:00 - 17:00:00", str(availability))

    def test_get_day_of_week_display(self):
        """Test de l'affichage du jour de la semaine"""
        availability = AvailabilityEmployee(
            employee=self.employee,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
            day_of_week=5,  # Samedi
            start_time=time(10, 0),
            end_time=time(14, 0)
        )
        self.assertEqual(availability.get_day_of_week_display(), "Samedi")

    def test_days_of_week_choices(self):
        """Test que tous les jours de la semaine sont disponibles"""
        days = dict(AvailabilityEmployee.DAYS_OF_WEEK)
        self.assertEqual(len(days), 7)
        self.assertEqual(days[4], "Vendredi")


class AvailabilityExceptionModelTest(TestCase):
    """Tests simples pour le modèle AvailabilityException"""

    def setUp(self):
        """Préparation des données de test"""
        person = Person(
            first_name='Bob',
            last_name='Johnson',
            phone=555123456,
            email='bob.johnson@example.com',
            birthday=date(1988, 9, 10)
        )
        person.set_password('password')
        person.save()

        role = Role.objects.create(name="Assistant")

        self.employee = Employee.objects.create(
            person=person,
            first_engagement_date=date(2022, 3, 1),
            role=role
        )

    def test_str_representation_available(self):
        """Test de la représentation string quand disponible"""
        exception = AvailabilityException(
            employee=self.employee,
            start_date=datetime(2025, 7, 14, 14, 0),
            end_date=datetime(2025, 7, 14, 18, 0),
            is_available=True
        )
        self.assertIn("Disponible", str(exception))

    def test_str_representation_unavailable(self):
        """Test de la représentation string quand indisponible"""
        exception = AvailabilityException(
            employee=self.employee,
            start_date=datetime(2025, 8, 1, 0, 0),
            end_date=datetime(2025, 8, 15, 23, 59),
            is_available=False
        )
        self.assertIn("Indisponible", str(exception))

    def test_is_available_default_value(self):
        """Test que is_available est False par défaut"""
        exception = AvailabilityException(
            employee=self.employee,
            start_date=datetime(2025, 1, 1, 0, 0),
            end_date=datetime(2025, 1, 1, 23, 59)
        )
        self.assertFalse(exception.is_available)