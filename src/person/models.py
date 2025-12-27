from django.db import models


class Person(models.Model):
    """Personnes qui interagissent avec le cabinet vétérinaire"""

    first_name = models.CharField(max_length=100, verbose_name="Prénom", null=False)

    last_name = models.CharField(max_length=100, verbose_name="Nom", null=False)

    phone = models.IntegerField(verbose_name="Numéro de téléphone")

    email = models.CharField(max_length=255)

    birthday = models.DateField(verbose_name="Date de naissance")

    password_hash = models.CharField(verbose_name="Mot de passe")

    class Meta:
        verbose_name = "Personne"
        verbose_name_plural = "Personnes"

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
