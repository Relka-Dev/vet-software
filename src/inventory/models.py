from django.db import models


class TreatmentType(models.Model):
    """Types de traitements (vaccination, consultation, chirurgie, etc.)"""

    type = models.CharField(max_length=100, verbose_name="Type de traitement")

    class Meta:
        verbose_name = "Type de traitement"
        verbose_name_plural = "Types de traitements"
        ordering = ['type']

    def __str__(self):
        return self.type


class Item(models.Model):
    """Articles/Produits utilisés dans les traitements"""

    treatment_type = models.ForeignKey(
        TreatmentType,
        on_delete=models.PROTECT,
        related_name='items',
        verbose_name="Type de traitement",
    )

    name = models.CharField(max_length=150, verbose_name="Nom de l'article")

    reminder = models.BooleanField(default=False, verbose_name="Rappel nécessaire")

    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Prix (CHF)"
    )

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.price} CHF"


class Inventory(models.Model):
    """Stock des articles"""

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='inventory',
        verbose_name="Article",
        null=False,
    )

    quantity = models.IntegerField(default=0, verbose_name="Quantité en stock")

    expiration_date = models.DateField(null=False, verbose_name="Date d'expiration")

    class Meta:
        verbose_name = "Inventaire"
        verbose_name_plural = "Inventaires"

    def __str__(self):
        return f"{self.item.name}: {self.quantity} unités"
