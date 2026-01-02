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


class OpenHours(models.Model):
    """Heures d'ouverture du cabinet vétérinaire"""

    DAYS_OF_WEEK = [
        (0, "Lundi"),
        (1, "Mardi"),
        (2, "Mercredi"),
        (3, "Jeudi"),
        (4, "Vendredi"),
        (5, "Samedi"),
        (6, "Dimanche"),
    ]

    start_date = models.DateField()
    end_date = models.DateField()
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name = "Heure d'ouverture"
        verbose_name_plural = "Heures d'ouverture"

    def __str__(self):
        return f"{self.get_day_of_week_display()} : {self.start_time} - {self.end_time} ({self.start_date} to {self.end_date})"


class OpenException(models.Model):
    """Exceptions aux heures d'ouverture du cabinet vétérinaire (pas implémenté)"""

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_open = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Exception aux heures d'ouverture"
        verbose_name_plural = "Exceptions aux heures d'ouverture"

    def __str__(self):
        status = "Ouvert" if self.is_open else "Fermé"
        return f"{self.start_date} to {self.end_date} : {status}"


class AvailabilityEmployee(models.Model):
    """Table d'association entre employés et périodes"""

    DAYS_OF_WEEK = [
        (0, "Lundi"),
        (1, "Mardi"),
        (2, "Mercredi"),
        (3, "Jeudi"),
        (4, "Vendredi"),
        (5, "Samedi"),
        (6, "Dimanche"),
    ]

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name="Employé(e)"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.employee} - {self.get_day_of_week_display()} : {self.start_time} - {self.end_time} ({self.start_date} to {self.end_date})"


class AvailabilityException(models.Model):
    """Exceptions aux disponibilités des employés (pas implémenté)"""

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name="Employé(e)"
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_available = models.BooleanField(default=False)

    def __str__(self):
        status = "Disponible" if self.is_available else "Indisponible"
        return f"{self.employee} - {self.start_date} to {self.end_date} : {status}"
