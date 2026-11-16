from django.contrib import admin
from django.utils import timezone
from .models import Category, ServiceRequest, WorkOrder, Comment

class OverdueListFilter(admin.SimpleListFilter):
    title = 'overdue status'
    parameter_name = 'overdue'

    def lookups(self, request, model_admin):
        return (
            ('overdue', 'Overdue'),
            ('upcoming', 'Due in Future'),
        )

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == 'overdue':
            return queryset.filter(due_at__lt=now).exclude(status__in=[ServiceRequest.Status.RESOLVED, ServiceRequest.Status.CLOSED])
        if self.value() == 'upcoming':
            return queryset.filter(due_at__gte=now)
        return queryset

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name',)

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'requester', 'category', 'priority', 'status', 'due_at', 'created_at')
    list_filter = ('status', 'priority', 'category', OverdueListFilter)
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('service_request', 'technician', 'started_at', 'completed_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('service_request', 'author', 'is_internal', 'created_at')