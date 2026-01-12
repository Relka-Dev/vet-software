from django.test import TestCase
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from datetime import date
from .models import Person


class PersonModelTest(TestCase):

    def setUp(self):
        """Préparation des données de test"""
        self.person_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': 123456789,
            'email': 'john.doe@example.com',
            'birthday': date(1990, 5, 15)
        }

    def test_create_person(self):
        """Test de création d'une personne"""
        person = Person(**self.person_data)
        person.set_password('password123')
        person.save()
        
        self.assertEqual(person.first_name, 'John')
        self.assertEqual(person.last_name, 'Doe')
        self.assertEqual(person.email, 'john.doe@example.com')
        self.assertEqual(person.phone, 123456789)
        self.assertEqual(person.birthday, date(1990, 5, 15))
        self.assertIsNotNone(person.password_hash)

    def test_set_password_hashes_correctly(self):
        """Test que set_password hash correctement le mot de passe"""
        person = Person(**self.person_data)
        raw_password = 'secure_password_456'
        
        person.set_password(raw_password)
        
        self.assertNotEqual(person.password_hash, raw_password)
        self.assertTrue(check_password(raw_password, person.password_hash))
        self.assertFalse(check_password('wrong_password', person.password_hash))

    def test_get_full_name(self):
        """Test de la méthode get_full_name"""
        person = Person(**self.person_data)
        
        self.assertEqual(person.get_full_name(), 'John Doe')

    def test_username_property(self):
        """Test de la propriété username"""
        person = Person(**self.person_data)
        
        self.assertEqual(person.username, 'John Doe')

    def test_is_authenticated_property(self):
        """Test de la propriété is_authenticated"""
        person = Person(**self.person_data)
        
        self.assertTrue(person.is_authenticated)

    def test_is_anonymous_property(self):
        """Test de la propriété is_anonymous"""
        person = Person(**self.person_data)
        
        self.assertFalse(person.is_anonymous)

    def test_str_representation(self):
        """Test de la représentation string"""
        person = Person(**self.person_data)
        
        self.assertEqual(str(person), 'Doe, John')

    def test_email_uniqueness(self):
        """Test que l'email doit être unique"""
        person1 = Person(**self.person_data)
        person1.set_password('pass1')
        person1.save()
        
        duplicate_data = self.person_data.copy()
        duplicate_data['first_name'] = 'Marie'
        person2 = Person(**duplicate_data)
        person2.set_password('pass2')
        
        with self.assertRaises(Exception):
            person2.save()

    def test_last_login_field(self):
        """Test du champ last_login"""
        person = Person(**self.person_data)
        person.set_password('pass')
        person.save()
        
        self.assertIsNone(person.last_login)
        
        now = timezone.now()
        person.last_login = now
        person.save()
        person.refresh_from_db()
        
        self.assertIsNotNone(person.last_login)

    def test_multiple_password_changes(self):
        """Test de changements multiples de mot de passe"""
        person = Person(**self.person_data)
        
        person.set_password('password1')
        hash1 = person.password_hash
        self.assertTrue(check_password('password1', hash1))
        
        person.set_password('password2')
        hash2 = person.password_hash
        self.assertTrue(check_password('password2', hash2))
        self.assertFalse(check_password('password1', hash2))
        
        self.assertNotEqual(hash1, hash2)