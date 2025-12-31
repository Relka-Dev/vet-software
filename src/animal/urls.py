from django.urls import path
from . import views

urlpatterns = [
    path('', views.animal_list, name='animal_list'),
    path(
        'note/<int:animal_pk>/',
        views.display_animal_note,
        {'note_pk': None},
        name='animal_note_by_animal',
    ),
    path(
        'note/<int:animal_pk>/<int:note_pk>/',
        views.display_animal_note,
        name='animal_note',
    ),
    path(
        'family_contacts/<int:pk>/',
        views.animal_family_contacts,
        name='animal_family_contacts',
    ),
    path('add_animal/', views.add_animal, name='add_animal'),
    path('update_animal/<int:pk>/', views.update_animal, name='update_animal'),
]
