from django.urls import path
from . import views

urlpatterns = [
    path('', views.family_list, name='family_list'),
    path(
        'family_contacts/<int:pk>/',
        views.family_contacts,
        name='family_contacts',
    ),
    path(
        'edit_family_member/<int:family_pk>/<int:person_pk>',
        views.edit_family_member,
        name='edit_family_member',
    ),
]
