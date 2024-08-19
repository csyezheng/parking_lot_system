from django.db import models


class ParkingLot(models.Model):
    name = models.CharField(max_length=50, unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


class ParkingTransaction(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=20)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True, blank=True)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.license_plate} at {self.parking_lot.name}"


class ParkingHistory(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    date = models.DateField()
    occupancy_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.parking_lot.name} - {self.date} - Occupancy: {self.occupancy_rate}% - Revenue: ${self.total_revenue}"


class HourlyOccupancy(models.Model):
    date = models.DateField()
    hour = models.TimeField()
    occupancy_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.date} {self.hour} - Occupancy: {self.occupancy_rate}%"

