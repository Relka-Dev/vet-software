from django.shortcuts import render
from .models import Inventory


def inventory_list(request):
    inventory = Inventory.objects.all()
    return render(request, 'inventory/inventory_list.html', {'inventory': inventory})
