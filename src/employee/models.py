from django.db import models
from person.models import Person

class Role(models.Model):
    """Fonctions liées aux employés (vétérinaire, réceptioniste, étudiant etc.)"""
    name = models.CharField(
        max_length=100,
        verbose_name="Fonction de l'employé(e)"
    )

    class Meta:
        verbose_name = "Fonction de l'employé(e)"
        verbose_name_plural = "Fonctions de l'employé(e)"


class Employee(models.Model):
    """Employés du cabinet vétérinaire"""

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="employee",
        verbose_name="Personne"
    )

    first_engagement_date = models.DateField()

    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name="employee",
        verbose_name="Fonction de l'employé(e)"
    )

    class Meta:
        verbose_name = "Employé(e)"
        verbose_name_plural = "Employé(e)s"


class DisponibilityRange(models.Model):
    """Périodes de temps"""

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        verbose_name = "Période de disponibilité"
        verbose_name_plural = "Périodes de disponibilité"


class DisponibilityEmployee(models.Model):
    """Table d'association entre employés et périodes"""

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name="Employé(e)"
    )
    disponibility_range = models.ForeignKey(
        DisponibilityRange,
        on_delete=models.CASCADE,
        verbose_name="Période"
    )
