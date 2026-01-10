from django.urls import path
from . import views

urlpatterns = [
    path('', views.family_list, name='family_list'),
    path(
        'family_contacts/<int:pk>/',
        views.family_contacts,
        name='family_contacts',
    ),
    path('add_family', views.add_family, name='add_family'),
    path(
        'add_family_member/<int:family_pk>',
        views.add_family_member,
        name='add_family_member',
    ),
    path(
        'edit_family_member/<int:family_pk>/<int:person_pk>',
        views.edit_family_member,
        name='edit_family_member',
    ),
]
