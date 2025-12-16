from django.db import models
from animal.models import Animal
from employee.models import Employee

class RoomType(models.Model):
    """Types de salles (consulation, opération, radio, etc.)"""

    name = models.CharField(
        max_length=50,
        verbose_name="Type de salle"
    )

    class Meta:
        verbose_name = "Type de salle"
        verbose_name_plural = "Types de salle"


class Room(models.Model):
    """Salles dans le cabinet vétérinaire"""

    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.PROTECT,
        related_name="room",
        verbose_name="Type de salle"
    )

    class Meta:
        verbose_name = "Salles"
        verbose_name_plural = "Salles"


class EmergencyType(models.Model):
    """Types d'urgence/consultation"""

    name = models.CharField(
        max_length=100,
        verbose_name="Type de rendez-vous"
    )

    class Meta:
        verbose_name = "Type de rendez-vous"
        verbose_name_plural = "Types de rendez-vous"

class Procedure(models.Model):
    """Types de procédure fait durant une consultation"""

    name = models.CharField(
        max_length=100,
        verbose_name="Nom de la prodécure"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix (CHF)"
    )

    class Meta:
        verbose_name = "Procédure"
        verbose_name_plural = "Procédures"

class Equipement(models.Model):
    """Types d'équipement utilisés durant une consultation"""

    name = models.CharField(
        max_length=50,
        verbose_name="Nom de l'équipement"
    )

    class Meta:
        verbose_name = "Équipement"
        verbose_name_plural = "Équipements"


class Appointement(models.Model):
    """Informations sur les rendez-vous/consultations"""

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="appointement",
        verbose_name="Animal"
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name="appointement",
        verbose_name="Salle"
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="appointement",
        verbose_name="Employé"
    )

    emergency_type = models.ForeignKey(
        EmergencyType,
        on_delete=models.PROTECT,
        related_name="appointement",
        verbose_name="Type de consultation"
    )

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        verbose_name = "Consultation"
        verbose_name_plural = "Consultations"


class AppointementProcedure(models.Model):
    """Table d'association entre consultation et prodécure"""

    appointement = models.ForeignKey(
        Appointement,
        on_delete=models.PROTECT,
        verbose_name="Consultation"
    )

    prodecure = models.ForeignKey(
        Procedure,
        on_delete=models.PROTECT,
        verbose_name="Procédure"
    )

    quantity = models.IntegerField()

    class Meta:
        verbose_name = "Association consultation/procédure"
        verbose_name_plural = "Associations consultation/procédure"

class AppointementEquipement(models.Model):
    """Table d'association entre consultation et équipements"""

    appointement = models.ForeignKey(
        Appointement,
        on_delete=models.PROTECT,
        verbose_name="Consultation"
    )

    equipement = models.ForeignKey(
        Procedure,
        on_delete=models.PROTECT,
        verbose_name="Équipement"
    )

    class Meta:
        verbose_name = "Association consultation/équipement"
        verbose_name_plural = "Associations consultation/équipement"
