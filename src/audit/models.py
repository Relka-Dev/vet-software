from django.db import models
from person.models import Person


class ActivityLog(models.Model):
    """
    Modèle pour enregistrer les activités utilisateur.
    """

    ACTION_CHOICES = [
        ('CREATE', 'Création'),
        ('UPDATE', 'Modification'),
        ('DELETE', 'Suppression'),
    ]

    user = models.ForeignKey(
        'person.Person',  # Référence explicitement Person, pas User
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    action = models.CharField(
        max_length=10,
        choices=ACTION_CHOICES,
    )
    object_type = models.CharField(
        max_length=100,
    )
    object_name = models.CharField(
        max_length=200,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Journal d'activité"
        verbose_name_plural = "Journal d'activités"

    def __str__(self):
        return f"{self.action} - {self.object_type}: {self.object_name}"
