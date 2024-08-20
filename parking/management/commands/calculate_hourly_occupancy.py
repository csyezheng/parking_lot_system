from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from parking.models import ParkingTransaction, ParkingLot, HourlyOccupancy


class Command(BaseCommand):
    help = 'Calculate and save hourly occupancy rates'

    def handle(self, *args, **kwargs):
        # Define the date range for the calculation, e.g., yesterday
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=32)

        parking_lots = ParkingLot.objects.all()

        for parking_lot in parking_lots:
            # Calculate hourly occupancy for each hour of the previous day
            for hour in range(24):
                hour_start = make_aware(datetime.combine(start_date, datetime.min.time()) + timedelta(hours=hour))
                hour_end = hour_start + timedelta(hours=1)

                # Count the number of vehicles that were parked during this hour
                occupancy_count = ParkingTransaction.objects.filter(
                    parking_lot=parking_lot,
                    entry_time__lt=hour_end,
                    exit_time__gte=hour_start
                ).count()

                # Calculate occupancy rate
                occupancy_rate = (occupancy_count / parking_lot.capacity) * 100

                # Save the data into the HourlyOccupancy model
                HourlyOccupancy.objects.update_or_create(
                    parking_lot=parking_lot,
                    date=start_date,
                    hour=hour_start.time(),
                    defaults={'occupancy_rate': occupancy_rate},
                )

        self.stdout.write(self.style.SUCCESS('Successfully calculated and saved hourly occupancy rates.'))
