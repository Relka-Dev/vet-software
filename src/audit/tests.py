from django.test import TestCase
from datetime import date
from person.models import Person
from .models import ActivityLog


class ActivityLogModelTest(TestCase):
    """Tests simples pour le modèle ActivityLog"""

    def setUp(self):
        """Préparation des données de test"""
        self.person = Person(
            first_name='John',
            last_name='Doe',
            phone=123456789,
            email='john.log@example.com',
            birthday=date(1985, 3, 15)
        )
        self.person.set_password('password')
        self.person.save()

    def test_str_representation(self):
        """Test de la représentation string"""
        log = ActivityLog(
            user=self.person,
            action='CREATE',
            object_type='Animal',
            object_id=42
        )
        self.assertEqual(str(log), "CREATE - Animal: 42")

    def test_action_choices(self):
        """Test que les choix d'actions sont disponibles"""
        choices_dict = dict(ActivityLog.ACTION_CHOICES)
        self.assertEqual(choices_dict['CREATE'], 'Création')
        self.assertEqual(choices_dict['UPDATE'], 'Modification')
        self.assertEqual(choices_dict['DELETE'], 'Suppression')
        self.assertEqual(len(choices_dict), 3)

    def test_timestamp_auto_add(self):
        """Test que timestamp est automatique"""
        log = ActivityLog.objects.create(
            user=self.person,
            action='UPDATE',
            object_type='Appointment',
            object_id=10
        )
        self.assertIsNotNone(log.timestamp)

    def test_details_can_be_blank(self):
        """Test que details peut être vide"""
        log = ActivityLog(
            user=self.person,
            action='DELETE',
            object_type='Treatment',
            object_id=5
        )
        self.assertEqual(log.details, '')

    def test_user_can_be_null(self):
        """Test que user peut être NULL"""
        log = ActivityLog(
            user=None,
            action='CREATE',
            object_type='Item',
            object_id=99
        )
        self.assertIsNone(log.user)

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(ActivityLog._meta.verbose_name, "Journal d'activité")
        self.assertEqual(ActivityLog._meta.verbose_name_plural, "Journal d'activités")

    def test_ordering(self):
        """Test de l'ordre par défaut (timestamp décroissant)"""
        self.assertEqual(ActivityLog._meta.ordering, ['-timestamp'])

    def test_get_action_display(self):
        """Test de l'affichage de l'action en français"""
        log = ActivityLog(
            user=self.person,
            action='UPDATE',
            object_type='Family',
            object_id=7
        )
        self.assertEqual(log.get_action_display(), 'Modification')