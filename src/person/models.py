from django.db import models

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(
        max_length=100,
        verbose_name="Prénom"
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="Nom"
    )
    phone = models.IntegerField(
        verbose_name = "numéro de téléphone"
    )
    email = models.CharField(
        max_length=255
    )
    birthday = models.DateField(
        verbose_name="date de naissance"
    )

    password_hash = models.CharField(
        verbose_name="mot de pass"
    )
