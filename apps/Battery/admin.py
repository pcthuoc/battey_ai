from django.contrib import admin
from .models import Battery

@admin.register(Battery)
class BatteryAdmin(admin.ModelAdmin):
    list_display = ('name', 'nominal_capacity', 'voltage_min', 'voltage_max', 'date_added')
    search_fields = ('name',)
    list_filter = ('date_added',)
    ordering = ('-date_added',)
