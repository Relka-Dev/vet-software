from django.test import TestCase
from datetime import date
from person.models import Person
from .models import Family, Extra_family_member


class FamilyModelTest(TestCase):
    """Tests simples pour le modèle Family"""

    def setUp(self):
        """Préparation des données de test"""
        self.person = Person(
            first_name='John',
            last_name='Doe',
            phone=123456789,
            email='john.doe@example.com',
            birthday=date(1980, 1, 1)
        )
        self.person.set_password('password')
        self.person.save()

    def test_str_representation(self):
        """Test de la représentation string"""
        family = Family(main_contact=self.person)
        self.assertEqual(str(family), "Doe, John")

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(Family._meta.verbose_name, "Famille")
        self.assertEqual(Family._meta.verbose_name_plural, "Familles")

    def test_creation_date_auto(self):
        """Test que creation_date est automatique"""
        family = Family.objects.create(main_contact=self.person)
        self.assertIsNotNone(family.creation_date)
        self.assertEqual(family.creation_date, date.today())


class ExtraFamilyMemberModelTest(TestCase):
    """Tests simples pour le modèle Extra_family_member"""

    def setUp(self):
        """Préparation des données de test"""
        self.main_person = Person(
            first_name='John',
            last_name='Doe',
            phone=123456789,
            email='john.doe@example.com',
            birthday=date(1980, 1, 1)
        )
        self.main_person.set_password('password1')
        self.main_person.save()

        self.family = Family.objects.create(main_contact=self.main_person)

        self.extra_person = Person(
            first_name='Jane',
            last_name='Doe',
            phone=987654321,
            email='jane.doe@example.com',
            birthday=date(1985, 5, 15)
        )
        self.extra_person.set_password('password2')
        self.extra_person.save()

    def test_str_representation(self):
        """Test de la représentation string"""
        member = Extra_family_member(
            family=self.family,
            person=self.extra_person
        )
        expected = f"Family : {self.family} - Person : {self.extra_person}"
        self.assertEqual(str(member), expected)

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(Extra_family_member._meta.verbose_name, "Membre")
        self.assertEqual(Extra_family_member._meta.verbose_name_plural, "Membres")