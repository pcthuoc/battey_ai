# apps/Battery/models.py
import uuid
from django.db import models

class Battery(models.Model):
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Tạo mã định danh duy nhất
    name = models.CharField(max_length=50)
    nominal_capacity = models.FloatField()
    voltage_min = models.FloatField(default=2.75)
    voltage_max = models.FloatField(default=4.2)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.nominal_capacity}mAh - {self.identifier}"
