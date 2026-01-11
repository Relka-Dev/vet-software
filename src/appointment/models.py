from django.db import models
from animal.models import Animal
from employee.models import Employee
from inventory.models import Item


class RoomType(models.Model):
    """Types de salles (consultation, opération, radio, etc.)"""

    name = models.CharField(max_length=50, verbose_name="Type de salle", null=False)

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
        return str(self.room_type)


class EmergencyType(models.Model):
    """Types d'urgence/consultation"""

    name = models.CharField(
        max_length=100, verbose_name="Type de rendez-vous", null=False
    )

    class Meta:
        verbose_name = "Type de rendez-vous"
        verbose_name_plural = "Types de rendez-vous"

    def __str__(self):
        return self.name


class Procedure(models.Model):
    """Types de procédure fait durant une consultation"""

    name = models.CharField(
        max_length=100, verbose_name="Nom de la procédure", null=False
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Prix (CHF)"
    )

    class Meta:
        verbose_name = "Procédure"
        verbose_name_plural = "Procédures"

    def __str__(self):
        return f"{self.name} - {self.price} CHF"


class Equipment(models.Model):
    """Types d'équipement utilisés durant une consultation"""

    name = models.CharField(
        max_length=50, verbose_name="Nom de l'équipement", null=False
    )

    class Meta:
        verbose_name = "Équipement"
        verbose_name_plural = "Équipements"

    def __str__(self):
        return self.name


class Appointment(models.Model):
    """Informations sur les rendez-vous/consultations"""

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="appointment",
        verbose_name="Animal",
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name="appointment",
        verbose_name="Salle",
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="appointment",
        verbose_name="Employé",
    )

    emergency_type = models.ForeignKey(
        EmergencyType,
        on_delete=models.PROTECT,
        related_name="appointment",
        verbose_name="Type de consultation",
    )

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        verbose_name = "Consultation"
        verbose_name_plural = "Consultations"

    def clean(self):
        from django.core.exceptions import ValidationError

        conflicting = Appointment.objects.filter(
            employee=self.employee,
            start_date__lt=self.end_date,
            end_date__gt=self.start_date
        )

        if self.pk:
            conflicting = conflicting.exclude(pk=self.pk)

        if conflicting.exists():
            raise ValidationError(
                f"{self.employee.person.get_full_name()} a déjà un rendez-vous à cette période."
            )

    def __str__(self):
        return f"Animal : {self.animal} - Salle : {self.room} - Employee : {self.employee} - Emergency Type : {self.emergency_type} - Start Date  : {self.start_date} - End Date : {self.end_date}"


class AppointmentProcedure(models.Model):
    """Table d'association entre consultation et procédure"""

    appointment = models.ForeignKey(
        Appointment, on_delete=models.PROTECT, verbose_name="Consultation"
    )

    procedure = models.ForeignKey(
        Procedure, on_delete=models.PROTECT, verbose_name="Procédure"
    )

    quantity = models.IntegerField()

    class Meta:
        verbose_name = "Association consultation/procédure"
        verbose_name_plural = "Associations consultation/procédure"

    def __str__(self):
        return f"Appointment : {self.appointment} - Created By : {self.procedure} - Quantity : {self.quantity}"


class AppointmentEquipment(models.Model):
    """Table d'association entre consultation et équipements"""

    appointment = models.ForeignKey(
        Appointment, on_delete=models.PROTECT, verbose_name="Consultation"
    )

    equipment = models.ForeignKey(
        Equipment, on_delete=models.PROTECT, verbose_name="Équipement"
    )

    class Meta:
        verbose_name = "Association consultation/équipement"
        verbose_name_plural = "Associations consultation/équipement"

    def __str__(self):
        return f"Appointment : {self.appointment} - Created By : {self.equipment}"


class AppointmentItem(models.Model):
    """Table d'association entre consultation et articles utilisés"""

    appointment = models.ForeignKey(
        Appointment, on_delete=models.PROTECT, verbose_name="Consultation"
    )

    item = models.ForeignKey(Item, on_delete=models.PROTECT, verbose_name="Article")

    quantity = models.IntegerField()

    class Meta:
        verbose_name = "Association consultation/article"
        verbose_name_plural = "Associations consultation/article"

    def __str__(self):
        return f"Appointment : {self.item} - Created By : {self.quantity}"
