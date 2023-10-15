from django.contrib import admin, messages
from .models import Monitor, Asset, Quotation

class MonitorAdmin(admin.ModelAdmin):
    list_display =['asset', 'interval', 'active'] 
    exclude = ('task',)

    def delete_queryset(self, request, queryset):
        for monitor in queryset:
            monitor.task.interval.delete()
            monitor.task.delete()
        queryset.delete()
        
class QuotationAdmin(admin.ModelAdmin):
    list_display =['asset', 'price', 'recording_date', 'trade_date'] 
    search_fields = ['asset__name', 'price'] 
class AssetAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        try:
            return super(AssetAdmin, self).save_model(request, obj, form, change)
        except ValueError as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request, e)           

admin.site.register(Monitor, admin_class=MonitorAdmin)
admin.site.register(Asset, admin_class=AssetAdmin)
admin.site.register(Quotation, admin_class=QuotationAdmin)
