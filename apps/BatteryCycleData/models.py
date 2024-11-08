from django.db import models
from apps.Battery.models import Battery
from apps.BatteryProcessLog.models import BatteryProcessLog

class BatteryCycleData(models.Model):
    battery = models.ForeignKey(Battery, on_delete=models.CASCADE, related_name='cycle_data')
    process = models.ForeignKey(BatteryProcessLog, on_delete=models.CASCADE, related_name='cycle_data')
    cycle_number = models.IntegerField()
    voltage = models.FloatField()
    current = models.FloatField()
    temperature = models.FloatField()
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['battery', 'timestamp']),
            models.Index(fields=['process', 'cycle_number']),
        ]

    def __str__(self):
        return f"Cycle {self.cycle_number} - {self.battery.name} ({self.timestamp})"
