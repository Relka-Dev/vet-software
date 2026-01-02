from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('<int:year>/', views.dashboard_view, name='dashboard_year'),
]
