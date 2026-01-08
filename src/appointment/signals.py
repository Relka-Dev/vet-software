from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import AppointmentItem
from inventory.models import Item, Inventory


@receiver(pre_save, sender=AppointmentItem)
# Stocke l'ancienne quantité avant la sauvegarde
def store_old_quantity(sender, instance, **kwargs):
    if instance.pk:  # Si l'objet existe déjà
        try:
            old_instance = AppointmentItem.objects.get(pk=instance.pk)
            instance._old_quantity = old_instance.quantity
        except AppointmentItem.DoesNotExist:
            instance._old_quantity = 0
    else:
        instance._old_quantity = 0


@receiver(post_save, sender=AppointmentItem)
# Décrémente l'inventaire quand un item est ajouté ou modifié
def update_inventory_on_save(sender, instance, created, **kwargs):
    item = instance.item
    inventory_item = Inventory.objects.get(item=item)

    if created:
        # Nouvel item créé - décrémenter l'inventaire
        difference = instance.quantity
    else:
        # Item modifié - ajuster l'inventaire
        # Récupérer l'ancienne valeur depuis la base de données
        old_quantity = getattr(instance, '_old_quantity', 0)
        difference = instance.quantity - old_quantity

    if inventory_item.quantity >= difference:
        inventory_item.quantity -= difference
        inventory_item.save()
    else:
        raise ValueError(
            f"Stock insuffisant pour {item.name}. Disponible: {inventory_item.quantity}"
        )


""" # not sure if needed
@receiver(post_delete, sender=AppointmentItem)
def restore_inventory_on_delete(sender, instance, **kwargs):
    item = instance.item
    inventory_item = Inventory.objects.get(item=item)
    inventory_item.quantity += instance.quantity
    inventory_item.save()
"""
