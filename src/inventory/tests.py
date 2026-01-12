from django.test import TestCase
from datetime import date
from decimal import Decimal
from .models import TreatmentType, Item, Inventory


class TreatmentTypeModelTest(TestCase):
    """Tests simples pour le modèle TreatmentType"""

    def test_str_representation(self):
        """Test de la représentation string"""
        treatment_type = TreatmentType(type="Vaccination")
        self.assertEqual(str(treatment_type), "Vaccination")

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(TreatmentType._meta.verbose_name, "Type de traitement")
        self.assertEqual(TreatmentType._meta.verbose_name_plural, "Types de traitements")

    def test_ordering(self):
        """Test de l'ordre par défaut"""
        self.assertEqual(TreatmentType._meta.ordering, ['type'])


class ItemModelTest(TestCase):
    """Tests simples pour le modèle Item"""

    def setUp(self):
        """Préparation des données de test"""
        self.treatment_type = TreatmentType.objects.create(type="Consultation")

    def test_str_representation(self):
        """Test de la représentation string"""
        item = Item(
            treatment_type=self.treatment_type,
            name="Aspirine",
            price=Decimal("15.50")
        )
        self.assertEqual(str(item), "Aspirine - 15.50 CHF")

    def test_reminder_default_value(self):
        """Test que reminder est False par défaut"""
        item = Item(
            treatment_type=self.treatment_type,
            name="Bandage",
            price=Decimal("5.00")
        )
        self.assertFalse(item.reminder)

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(Item._meta.verbose_name, "Article")
        self.assertEqual(Item._meta.verbose_name_plural, "Articles")

    def test_ordering(self):
        """Test de l'ordre par défaut"""
        self.assertEqual(Item._meta.ordering, ['name'])

    def test_price_precision(self):
        """Test de la précision du prix"""
        item = Item(
            treatment_type=self.treatment_type,
            name="Médicament",
            price=Decimal("123.45")
        )
        self.assertEqual(item.price, Decimal("123.45"))


class InventoryModelTest(TestCase):
    """Tests simples pour le modèle Inventory"""

    def setUp(self):
        """Préparation des données de test"""
        treatment_type = TreatmentType.objects.create(type="Chirurgie")
        self.item = Item.objects.create(
            treatment_type=treatment_type,
            name="Seringue",
            price=Decimal("2.50")
        )

    def test_str_representation(self):
        """Test de la représentation string"""
        inventory = Inventory(
            item=self.item,
            quantity=100,
            expiration_date=date(2025, 12, 31)
        )
        self.assertEqual(str(inventory), "Seringue: 100 unités")

    def test_quantity_default_value(self):
        """Test que quantity est 0 par défaut"""
        inventory = Inventory(
            item=self.item,
            expiration_date=date(2025, 12, 31)
        )
        self.assertEqual(inventory.quantity, 0)

    def test_verbose_names(self):
        """Test des verbose_names"""
        self.assertEqual(Inventory._meta.verbose_name, "Inventaire")
        self.assertEqual(Inventory._meta.verbose_name_plural, "Inventaires")