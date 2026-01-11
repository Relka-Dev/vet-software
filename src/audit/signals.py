from django.db.models.signals import post_save, post_delete
from audit.models import ActivityLog
from animal.models import Animal, SOAPNote
from appointment.models import Appointment
from inventory.models import Inventory
from employee.models import Employee
from person.models import Person


def get_model_details(instance):
    """
    Retourne une chaîne avec tous les champs importants de l'instance.
    """
    details = []
    for field in instance._meta.get_fields():
        # Ignorer les relations reverse
        if field.auto_created:
            continue
        # Ignorer les relations many-to-many
        if field.many_to_many:
            continue
        # Ignorer les champs spéciaux
        if field.name in ['_current_user']:
            continue
        try:
            value = getattr(instance, field.name, None)
            if value is not None:
                if hasattr(value, 'pk'):
                    value = f"{value.pk} ({str(value)})"
                details.append(f"{field.name}: {value}")
        except Exception:
            pass
    return ", ".join(details)


def log_activity(user, action, object_type, object_id, details=""):
    """
    Fonction pour enregistrer une activité.
    """
    if not isinstance(user, Person):
        return

    try:
        ActivityLog.objects.create(
            user=user,
            action=action,
            object_type=object_type,
            object_id=object_id,
            details=details,
        )
    except Exception:
        pass


def generic_log_change(sender, instance, created, **kwargs):
    """Signal générique pour CREATE/UPDATE"""
    action = 'CREATE' if created else 'UPDATE'
    user = getattr(instance, '_current_user', None)

    log_activity(
        user=user,
        action=action,
        object_type=instance.__class__.__name__,
        object_id=instance.id,
        details=get_model_details(instance),
    )


def generic_log_delete(sender, instance, **kwargs):
    """Signal générique pour DELETE"""
    user = getattr(instance, '_current_user', None)

    log_activity(
        user=user,
        action='DELETE',
        object_type=instance.__class__.__name__,
        object_id=instance.id,
        details=get_model_details(instance),
    )


# Connecter les signaux génériques à tous les modèles
post_save.connect(generic_log_change, sender=Animal, dispatch_uid='log_animal_change')
post_delete.connect(generic_log_delete, sender=Animal, dispatch_uid='log_animal_delete')

post_save.connect(
    generic_log_change, sender=SOAPNote, dispatch_uid='log_soapnote_change'
)
post_delete.connect(
    generic_log_delete, sender=SOAPNote, dispatch_uid='log_soapnote_delete'
)

post_save.connect(
    generic_log_change, sender=Appointment, dispatch_uid='log_appointment_change'
)
post_delete.connect(
    generic_log_delete, sender=Appointment, dispatch_uid='log_appointment_delete'
)

post_save.connect(
    generic_log_change, sender=Inventory, dispatch_uid='log_inventory_change'
)
post_delete.connect(
    generic_log_delete, sender=Inventory, dispatch_uid='log_inventory_delete'
)
