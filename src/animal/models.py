from django.db import models
from family.models import Family
from employee.models import Employee


class Species(models.Model):
    """Espèces des animaux"""

    name = models.CharField(max_length=50, verbose_name="Nom de l'espèce", unique=True)

    class Meta:
        verbose_name = "Espèce"
        verbose_name_plural = "Espèces"

    def __str__(self):
        return self.name


class Animal(models.Model):
    """Animaux pris en charge par le cabinet"""

    name = models.CharField(null=False, max_length=50, verbose_name="Nom de l'animal")
    birthday = models.DateField()
    death_date = models.DateField(null=True, blank=True)

    federal_identification = models.CharField(
        max_length=100, verbose_name="Identification fédérale"
    )

    family = models.ForeignKey(
        Family, on_delete=models.PROTECT, related_name="animal", verbose_name="Contact"
    )
    species = models.ForeignKey(
        "Species",
        on_delete=models.PROTECT,
        related_name="animals",
        verbose_name="Espèce",
    )

    class Meta:
        verbose_name = "Animal"
        verbose_name_plural = "Animaux"

    def __str__(self):
        return f"{self.species}: {self.name} {self.family.main_contact.last_name} ({self.birthday})"


class SOAPNote(models.Model):
    """Notes associées à une consultation"""

    content = models.TextField(max_length=500, verbose_name="Contenu de la SOAP note")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date de création"
    )

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="notes",
        verbose_name="Animal",
        null=False,
    )

    text_subjective = models.TextField(verbose_name="Texte subjectif")
    text_objective = models.TextField(verbose_name="Texte objectif")
    text_assessment = models.TextField(verbose_name="Texte d'évaluation")
    text_plan = models.TextField(verbose_name="Texte de planification")

    created_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="created_notes",
        verbose_name="Créé par",
    )

    validated_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="validated_notes",
        verbose_name="Validé par",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "SOAP Note"
        verbose_name_plural = "SOAP Notes"

    def __str__(self):
        return f"Content : {self.content} - Created at : {self.created_at} - Animal : {self.animal} - Created By : {self.created_by} - Validated By : {self.validated_by}"
