from django.contrib import admin
from .models import BatteryProcessLog

@admin.register(BatteryProcessLog)
class BatteryProcessLogAdmin(admin.ModelAdmin):
    list_display = ('battery', 'process_id', 'process_type', 'start_time', 'end_time')
    list_filter = ('process_type', 'start_time', 'end_time')
    search_fields = ('battery__name', 'process_id')
    ordering = ('-start_time',)
