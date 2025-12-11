from django.contrib import admin
from .models import TreatmentType, Item, Inventory

@admin.register(TreatmentType)
class TreatmentTypeAdmin(admin.ModelAdmin):
    list_display = ['type', 'item_count']
    search_fields = ['type']
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = "Nombre d'articles"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'treatment_type', 'price', 'reminder']
    list_filter = ['treatment_type', 'reminder']
    search_fields = ['name']
    list_editable = ['price', 'reminder']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'treatment_type')
        }),
        ('Détails', {
            'fields': ('price', 'reminder')
        }),
    )


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity', 'get_item_price']
    search_fields = ['item__name']
    list_editable = ['quantity']
    list_filter = ['item__treatment_type']
    
    def get_item_price(self, obj):
        return f"{obj.item.price} CHF"
    get_item_price.short_description = "Prix unitaire"