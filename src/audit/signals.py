from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from audit.models import ActivityLog
from animal.models import Animal, SOAPNote, Species
from family.models import Family
from employee.models import Employee


from person.models import Person


def log_activity(user, action, object_type, object_name, details=""):
    """
    Fonction pour enregistrer une activité.
    """
    print(
        f"[DEBUG log_activity] user={user}, user.id={user.id if user else 'None'}, type={type(user)}"
    )
    if not isinstance(user, Person):
        print(f"[AUDIT] log_activity ignoré : user n'est pas une Person ({user})")
        return
    # Vérifie que la Person existe en base
    try:
        person_in_db = Person.objects.get(pk=user.id)
        print(f"[DEBUG log_activity] Person existe en base : {person_in_db}")
    except Person.DoesNotExist:
        print(f"[ERROR log_activity] Person id={user.id} n'existe pas en base!")
        return

    print(
        f"[DEBUG log_activity] Création ActivityLog avec : user={user.id}, action={action}, object_type={object_type}, object_name={object_name}, details={details[:50] if details else ''}"
    )
    try:
        log = ActivityLog.objects.create(
            user=user,
            action=action,
            object_type=object_type,
            object_name=object_name,
            details=details,
        )
        print(f"[DEBUG log_activity] ActivityLog créé avec succès : id={log.id}")
    except Exception as e:
        print(
            f"[WARN log_activity] Impossible de créer le log (non-bloquant, l'action métier continue) : {type(e).__name__}: {e}"
        )


# signaux : enregistrer automatiquement les actions
@receiver(post_save, sender=Animal)
def log_animal_change(sender, instance, created, **kwargs):
    """S'exécute après la création ou modification d'un animal"""
    action = 'CREATE' if created else 'UPDATE'
    user = getattr(instance, '_current_user', None)
    print(f"[DEBUG signal] user initial = {user} (type={type(user)})")
    if isinstance(user, Employee):
        print(f"[DEBUG signal] user est Employee, récupère person")
        user = user.person
        print(f"[DEBUG signal] user.person = {user}")

    if not isinstance(user, Person):
        print(
            f"[AUDIT WARNING] _current_user n'est pas une Person : {user} (type={type(user)})"
        )
    details = f"Espèce: {instance.species.name if instance.species else 'N/A'}, Famille: {instance.family.main_contact}"

    log_activity(
        user=user,
        action=action,
        object_type='Animal',
        object_name=instance.name,
        details=details,
    )


@receiver(post_delete, sender=Animal)
def log_animal_delete(sender, instance, **kwargs):
    """S'exécute après la suppression d'un animal"""
    user = getattr(instance, '_current_user', None)
    if isinstance(user, Employee):
        user = user.person
    if not isinstance(user, Person):
        print(
            f"[AUDIT WARNING] _current_user n'est pas une Person : {user} (type={type(user)})"
        )
    log_activity(
        user=user,
        action='DELETE',
        object_type='Animal',
        object_name=instance.name,
        details=f"Espèce: {instance.species.name if instance.species else 'N/A'}",
    )


@receiver(post_save, sender=SOAPNote)
def log_soapnote_change(sender, instance, created, **kwargs):
    """S'exécute après la création ou modification d'une SOAP note"""
    action = 'CREATE' if created else 'UPDATE'
    log_activity(
        user=instance.created_by.person if instance.created_by else None,
        action=action,
        object_type='SOAP Note',
        object_name=f"Note pour {instance.animal.name}",
        details=f"Animal: {instance.animal.name}",
    )


@receiver(post_delete, sender=SOAPNote)
def log_soapnote_delete(sender, instance, **kwargs):
    """S'exécute après la suppression d'une SOAP note"""
    log_activity(
        user=None,
        action='DELETE',
        object_type='SOAP Note',
        object_name=f"Note pour {instance.animal.name}",
        details=f"Animal: {instance.animal.name}",
    )
