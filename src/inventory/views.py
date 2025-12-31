from django.shortcuts import redirect, render
from .models import Inventory, Item, TreatmentType


def inventory_list(request):
    inventory = Inventory.objects.all()
    all_types = TreatmentType.objects.all()

    return render(
        request,
        'inventory/inventory_list.html',
        {'inventory': inventory, 'all_types': all_types},
    )


def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        reminder = request.POST.get('reminder')
        price = request.POST.get('price')
        treatment_type_id = request.POST.get('treatment_type')
        treatment_type = TreatmentType.objects.get(id=treatment_type_id)
        Item.objects.create(
            name=name, reminder=reminder, price=price, treatment_type=treatment_type
        )

        quantity = request.POST.get('quantity')
        expiration_date = request.POST.get('expiration_date')
        Inventory.objects.create(
            item=Item.objects.last(), quantity=quantity, expiration_date=expiration_date
        )

    return redirect('inventory_list')


def update_item(request, pk):
    item = Item.objects.get(id=pk)

    if request.method == 'POST' and 'edit-button' in request.POST:
        item.name = request.POST.get('name')
        item.reminder = request.POST.get('reminder')
        item.price = request.POST.get('price')
        treatment_type_id = request.POST.get('treatment_type')
        item.treatment_type = TreatmentType.objects.get(id=treatment_type_id)
        item.save()

        return redirect('inventory_list')

    if request.method == 'POST' and 'delete-button' in request.POST:
        item.delete()
        return redirect('inventory_list')

    return render(request, 'inventory/update_item.html', {'item': item})
