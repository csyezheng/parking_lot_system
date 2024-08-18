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
    date = models.DateField()
    occupancy_rate = models.DecimalField(max_digits=5, decimal_places=2)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.date} - Occupancy: {self.occupancy_rate}% - Revenue: ${self.total_revenue}"


class HourlyOccupancy(models.Model):
    date = models.DateField()
    hour = models.TimeField()
    occupancy_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.date} {self.hour} - Occupancy: {self.occupancy_rate}%"


class MonthlyRevenue(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    month = models.DateField()  # Use the first day of the month or any other date format that helps identify the month
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.parking_lot.name} - {self.month.strftime('%B %Y')} - ${self.total_revenue}"