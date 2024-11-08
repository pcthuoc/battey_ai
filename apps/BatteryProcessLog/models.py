from django.db import models
from apps.Battery.models import Battery

class BatteryProcessLog(models.Model):
    battery = models.ForeignKey(Battery, on_delete=models.CASCADE, related_name='process_logs')
    process_id = models.CharField(max_length=50, unique=True)
    process_type = models.CharField(max_length=11, choices=[('charging', 'Charging'), ('discharging', 'Discharging')])
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Process {self.process_id} - {self.process_type} ({self.battery.name})"

    @staticmethod
    def get_next_process_id(battery):
        last_process = BatteryProcessLog.objects.filter(battery=battery).order_by('-id').first()
        if last_process:
            next_process_id = str(int(last_process.process_id) + 1)
        else:
            next_process_id = '0'
        return next_process_id
