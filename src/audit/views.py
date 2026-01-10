from django.shortcuts import render
from audit.models import ActivityLog
from django.contrib.auth.decorators import login_required


@login_required
def audit_logs(request):
    """Affiche les logs d'audit"""
    logs = ActivityLog.objects.all()
    return render(request, 'audit/logs_list.html', {'logs': logs})
