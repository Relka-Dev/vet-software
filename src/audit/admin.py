from django.contrib import admin
from audit.models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'action',
        'object_type',
        'object_name',
        'user',
        'details',
    )
    list_filter = ('action', 'object_type', 'timestamp', 'user')
    search_fields = ('object_name', 'user__username', 'details')
    readonly_fields = (
        'timestamp',
        'user',
        'action',
        'object_type',
        'object_name',
        'details',
    )
