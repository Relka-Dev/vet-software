from django.shortcuts import render
from audit.models import ActivityLog
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


@login_required
def audit_logs(request):
    """Affiche les logs d'audit"""
    logs_list = ActivityLog.objects.all().order_by('-timestamp')
    paginator = Paginator(logs_list, 10)
    page_number = request.GET.get('page')
    logs = paginator.get_page(page_number)
    return render(request, 'audit/logs_list.html', {'logs': logs})
