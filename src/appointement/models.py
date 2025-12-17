from django.db import models
from animal.models import Animal
from employee.models import Employee
from inventory.models import Item


class RoomType(models.Model):
    """Types de salles (consulation, opération, radio, etc.)"""

    name = models.CharField(max_length=50, verbose_name="Type de salle")

    class Meta:
        verbose_name = "Type de salle"
        verbose_name_plural = "Types de salle"

    def __str__(self):
        return self.name


class Room(models.Model):
    """Salles dans le cabinet vétérinaire"""

    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.PROTECT,
        related_name="room",
        verbose_name="Type de salle",
    )

    class Meta:
        verbose_name = "Salles"
        verbose_name_plural = "Salles"

    def __str__(self):
        return self.room_type


class EmergencyType(models.Model):
    """Types d'urgence/consultation"""

    name = models.CharField(max_length=100, verbose_name="Type de rendez-vous")

    class Meta:
        verbose_name = "Type de rendez-vous"
        verbose_name_plural = "Types de rendez-vous"

    def __str__(self):
        return self.name


class Procedure(models.Model):
    """Types de procédure fait durant une consultation"""

    name = models.CharField(max_length=100, verbose_name="Nom de la prodécure")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Prix (CHF)"
    )

    class Meta:
        verbose_name = "Procédure"
        verbose_name_plural = "Procédures"

    def __str__(self):
        return f"{self.name} - {self.price} CHF"


class Equipement(models.Model):
    """Types d'équipement utilisés durant une consultation"""

    name = models.CharField(max_length=50, verbose_name="Nom de l'équipement")

    class Meta:
        verbose_name = "Équipement"
        verbose_name_plural = "Équipements"

    def __str__(self):
        return self.name


class Appointement(models.Model):
    """Informations sur les rendez-vous/consultations"""

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="appointement",
        verbose_name="Animal",
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name="appointement",
        verbose_name="Salle",
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="appointement",
        verbose_name="Employé",
    )

    emergency_type = models.ForeignKey(
        EmergencyType,
        on_delete=models.PROTECT,
        related_name="appointement",
        verbose_name="Type de consultation",
    )

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        verbose_name = "Consultation"
        verbose_name_plural = "Consultations"

    def __str__(self):
        return f"Animal : {self.animal} - Salle : {self.room} - Employee : {self.employee} - Emergency Type : {self.emergency_type} - Start Date  : {self.start_date} - End Date : {self.end_date}"


class Note(models.Model):
    """Notes associées à une consultation"""

    content = models.TextField(max_length=500, verbose_name="Contenu de la note")

    created_at = models.DateTimeField(verbose_name="Date de création")

    appointement = models.ForeignKey(
        Appointement,
        on_delete=models.CASCADE,
        related_name="notes",
        verbose_name="Consultation",
    )

    created_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="notes",
        verbose_name="Créé par",
    )

    validated_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="validated_notes",
        verbose_name="Validé par",
    )

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"

    def __str__(self):
        return f"Content : {self.content} - Created at : {self.created_at} - Appointement : {self.appointement} - Created By : {self.created_at} - Validated By : {self.validated_by}"


class AppointementProcedure(models.Model):
    """Table d'association entre consultation et prodécure"""

    appointement = models.ForeignKey(
        Appointement, on_delete=models.PROTECT, verbose_name="Consultation"
    )

    prodecure = models.ForeignKey(
        Procedure, on_delete=models.PROTECT, verbose_name="Procédure"
    )

    quantity = models.IntegerField()

    class Meta:
        verbose_name = "Association consultation/procédure"
        verbose_name_plural = "Associations consultation/procédure"

    def __str__(self):
        return f"Appointement : {self.appointement} - Created By : {self.prodecure} - Quantity : {self.quantity}"


class AppointementEquipement(models.Model):
    """Table d'association entre consultation et équipements"""

    appointement = models.ForeignKey(
        Appointement, on_delete=models.PROTECT, verbose_name="Consultation"
    )

    equipement = models.ForeignKey(
        Procedure, on_delete=models.PROTECT, verbose_name="Équipement"
    )

    class Meta:
        verbose_name = "Association consultation/équipement"
        verbose_name_plural = "Associations consultation/équipement"

    def __str__(self):
        return f"Appointement : {self.appointement} - Created By : {self.equipement}"


class AppointementItem(models.Model):
    """Table d'association entre consultation et articles utilisés"""

    appointement = models.ForeignKey(
        Appointement, on_delete=models.PROTECT, verbose_name="Consultation"
    )

    item = models.ForeignKey(Item, on_delete=models.PROTECT, verbose_name="Article")

    quantity = models.IntegerField()

    class Meta:
        verbose_name = "Association consultation/article"
        verbose_name_plural = "Associations consultation/article"

    def __str__(self):
        return f"Appointement : {self.item} - Created By : {self.quantity}"
