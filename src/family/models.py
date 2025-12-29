from django.db import models
from person.models import Person


class Family(models.Model):
    """Membres d'une famille"""

    main_contact = models.ForeignKey(
        Person,
        on_delete=models.PROTECT,
        related_name="family",
        verbose_name="Contact principal",
        null=False,
    )
    creation_date = models.DateField()

    class Meta:
        verbose_name = "Famille"
        verbose_name_plural = "Familles"

    def __str__(self):
        return f"{str(self.main_contact)}"


class Extra_family_member(models.Model):
    """Membre d'une famille (qui n'est pas le contact principal)"""

    family = models.ForeignKey(
        Family,
        on_delete=models.PROTECT,
        related_name="extra",
        verbose_name="Contact",
        null=False,
    )

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="extra",
        verbose_name="Personne",
        null=False,
    )

    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"

    def __str__(self):
        return f"Family : {self.family} - Person : {self.person}"
