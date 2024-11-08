from django.contrib import admin
from .models import BatteryCycleData

@admin.register(BatteryCycleData)
class BatteryCycleDataAdmin(admin.ModelAdmin):
    list_display = ('id','battery', 'process', 'cycle_number', 'voltage', 'current', 'temperature', 'timestamp')
    list_filter = ('battery', 'timestamp')
    search_fields = ('battery__name', 'process__process_id')
    ordering = ('-timestamp',)
