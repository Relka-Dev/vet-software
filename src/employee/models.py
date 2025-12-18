from django.db import models
from person.models import Person


class Role(models.Model):
    """Fonctions liées aux employés (vétérinaire, réceptionniste, étudiant etc.)"""

    name = models.CharField(
        max_length=100, verbose_name="Fonction de l'employé(e)", null=False
    )

    class Meta:
        verbose_name = "Fonction de l'employé(e)"
        verbose_name_plural = "Fonctions de l'employé(e)"

    def __str__(self):
        return self.name


class Employee(models.Model):
    """Employés du cabinet vétérinaire"""

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="employee",
        verbose_name="Personne",
    )

    first_engagement_date = models.DateField()

    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name="employee",
        verbose_name="Fonction de l'employé(e)",
    )

    class Meta:
        verbose_name = "Employé(e)"
        verbose_name_plural = "Employé(e)s"

    def __str__(self):
        return f"{self.person} - {self.first_engagement_date} - {self.role}"


class AvailabilityRange(models.Model):
    """Périodes de temps"""

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        verbose_name = "Période de disponibilité"
        verbose_name_plural = "Périodes de disponibilité"

    def __str__(self):
        return f"Start Date : {self.start_date} - End Date : {self.end_date}"


class AvailabilityEmployee(models.Model):
    """Table d'association entre employés et périodes"""

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name="Employé(e)"
    )
    availability_range = models.ForeignKey(
        AvailabilityRange, on_delete=models.CASCADE, verbose_name="Période"
    )

    def __str__(self):
        return f"Employee : {self.employee} - Availability Range : {self.availability_range}"
