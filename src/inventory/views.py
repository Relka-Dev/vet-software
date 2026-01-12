from django.shortcuts import redirect, render
from .models import Inventory, Item, TreatmentType
from django.contrib.auth.decorators import login_required


@login_required

# function used to render database instances
def inventory_list(request):
    inventory = Inventory.objects.all()
    all_types = TreatmentType.objects.all()

    return render(
        request,
        'inventory/inventory_list.html',
        {'inventory': inventory, 'all_types': all_types},
    )


@login_required
def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        reminder = bool(request.POST.get('reminder'))
        price = request.POST.get('price')
        treatment_type_id = request.POST.get('treatment_type')
        treatment_type = TreatmentType.objects.get(id=treatment_type_id)
        # create the item first
        Item.objects.create(
            name=name, reminder=reminder, price=price, treatment_type=treatment_type
        )

        quantity = request.POST.get('quantity')
        expiration_date = request.POST.get('expiration_date')
        # create an "inventory" object with the item create before and its quantity
        Inventory.objects.create(
            item=Item.objects.last(), quantity=quantity, expiration_date=expiration_date
        )

    return redirect('inventory_list')


@login_required
def update_item(request, pk):
    # make sure it's the right item
    item = Item.objects.get(id=pk)
    inventory = Inventory.objects.get(item=item)

    # save the new informations with the edit button
    if request.method == 'POST' and 'edit-button' in request.POST:
        item.name = request.POST.get('name')
        item.reminder = bool(request.POST.get('reminder'))
        item.price = request.POST.get('price')
        treatment_type_id = request.POST.get('treatment_type')
        item.treatment_type = TreatmentType.objects.get(id=treatment_type_id)
        item._current_user = request.person
        item.save()

        inventory.quantity = request.POST.get('quantity')
        inventory.expiration_date = request.POST.get('expiration_date')
        inventory._current_user = request.person
        inventory.save()

        return redirect('inventory_list')

    # otherwise delete the item with the delete button
    if request.method == 'POST' and 'delete-button' in request.POST:
        item._current_user = request.person
        item.delete()
        return redirect('inventory_list')

    return redirect('inventory_list')
