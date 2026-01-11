from django.urls import path
from . import views

urlpatterns = [
    path('', views.audit_logs, name='logs'),
]
