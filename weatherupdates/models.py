from django.db import models

# Create your models here.
class Weatherupdates(models.Model):
    city = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    temperature = models.FloatField()
    wind = models.FloatField()
    humidity = models.FloatField()

    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.city} : {self.description}, {self.temperature}°C, as at {self.time_stamp} "