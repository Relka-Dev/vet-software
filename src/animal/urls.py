from django.urls import path
from . import views

urlpatterns = [
    path('', views.animal_list, name='animal_list'),
    path('note/<int:pk>/', views.display_animal_note, name='animal_note'),
]
