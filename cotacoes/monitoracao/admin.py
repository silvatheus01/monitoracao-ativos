from django.contrib import admin
from .models import Monitor, Asset, Quotation

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django_celery_beat.models import (PeriodicTask, IntervalSchedule, CrontabSchedule, SolarSchedule, ClockedSchedule)

def change_monitor_state(monitors, activate):
    monitors.update(active=activate)
    for monitor in monitors:
        monitor.task.enabled = activate
        monitor.task.save() 

@admin.action(description="Ativar monitores selecionados.")
def make_active(self, request, queryset):
    change_monitor_state(queryset, True)
    
@admin.action(description="Desativar monitores selecionados.")
def make_not_active(self, request, queryset):
    change_monitor_state(queryset, False)
    
class MonitorAdmin(admin.ModelAdmin):
    list_filter = ['active']
    list_display =['asset', 'interval', 'active'] 
    search_fields = ['asset__name', 'active'] 
    exclude = ('task',)
    actions = [make_active, make_not_active]
    
    def delete_queryset(self, request, queryset):
        for monitor in queryset:
            monitor.task.interval.delete()
            monitor.task.delete()
        queryset.delete()
        
class QuotationAdmin(admin.ModelAdmin):
    list_display =['asset', 'price', 'recording_date', 'trade_date'] 
    search_fields = ['asset__name', 'price', 'recording_date', 'trade_date'] 
    readonly_fields=['asset', 'price', 'recording_date', 'trade_date']
    list_filter = ['asset', 'recording_date', 'trade_date']
    list_per_page=10

    def has_add_permission(self, request):
        return False

class AssetAdmin(admin.ModelAdmin):
    list_display =['name'] 
    search_fields = ['name'] 

admin.site.register(Monitor, admin_class=MonitorAdmin)
admin.site.register(Asset, admin_class=AssetAdmin)
admin.site.register(Quotation, admin_class=QuotationAdmin)

admin.site.unregister([PeriodicTask, IntervalSchedule])
admin.site.unregister([CrontabSchedule, SolarSchedule, ClockedSchedule])

admin.site.unregister(User)
admin.site.unregister(Group)