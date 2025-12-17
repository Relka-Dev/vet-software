from django.db import models
from family.models import Family

class Animal(models.Model):
    """Animaux pris en charge par le cabinet"""

    name = models.CharField(
        max_length=50,
        verbose_name="Nom de l'animal"
    )
    birthday = models.DateField()

    federal_identification = models.CharField(
        max_length=100,
        verbose_name="Identification fédérale"
    )

    family = models.ForeignKey(
        Family,
        on_delete=models.PROTECT,
        related_name="animal",
        verbose_name="Contact"
    )

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animaux"


class AnimalChart(models.Model):
    """Dossier médical d'un animal"""

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="animal_chart",
        verbose_name="Animal"
    )

    class Meta:
        verbose_name = "Dossier médical"
        verbose_name_plural = "Dossiers médicaux"
