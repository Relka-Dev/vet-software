from django.shortcuts import render
from .models import Inventory, Item, TreatmentType


def inventory_list(request):
    inventory = Inventory.objects.all()
    return render(request, 'inventory/inventory_list.html', {'inventory': inventory})


def add_item(request):
    all_types = TreatmentType.objects.all()
    inventory = Inventory.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        reminder = request.POST.get('reminder')
        price = request.POST.get('price')
        treatment_type = request.POST.get('treatment_type')
        Item.objects.create(
            name=name, reminder=reminder, price=price, treatment_type=treatment_type
        )

        quantity = request.POST.get('quantity')
        expiration_date = request.POST.get('expiration_date')
        Inventory.objects.create(
            item=Item.objects.last(), quantity=quantity, expiration_date=expiration_date
        )

    return render(
        request,
        'inventory/inventory_list.html',
        {'inventory': inventory, 'all_types': all_types},
    )
