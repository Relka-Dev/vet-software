from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, verbose_name="Prénom", null=False)
    last_name = models.CharField(max_length=100, verbose_name="Nom", null=False)
    phone = models.IntegerField(verbose_name="Numéro de téléphone")
    email = models.CharField(max_length=255, unique=True)
    birthday = models.DateField(verbose_name="Date de naissance")
    password_hash = models.CharField(
        max_length=128, verbose_name="Mot de passe", null=True, blank=True
    )
    last_login = models.DateTimeField(null=True, blank=True)

    # Django authentication properties
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def username(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, raw_password):
        """Hash et sauvegarde le mot de passe"""
        self.password_hash = make_password(raw_password)

    class Meta:
        verbose_name = "Personne"
        verbose_name_plural = "Personnes"

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


# Signal pour créer automatiquement un User Django
@receiver(post_save, sender=Person)
def create_user_for_person(sender, instance, created, **kwargs):
    if created and not instance.user:
        user = User.objects.create(
            username=instance.email,
            email=instance.email,
            first_name=instance.first_name,
            last_name=instance.last_name,
            password=instance.password_hash,
        )
        Person.objects.filter(pk=instance.pk).update(user=user)
