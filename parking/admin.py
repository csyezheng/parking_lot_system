# admin.py
from django.contrib import admin
from .models import ParkingLot, ParkingTransaction, ParkingHistory, HourlyOccupancy


class ParkingLotAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')
    search_fields = ('name',)


class ParkingTransactionAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'parking_lot', 'entry_time', 'exit_time', 'revenue')
    list_filter = ('parking_lot', 'entry_time')
    search_fields = ('license_plate',)


class ParkingHistoryAdmin(admin.ModelAdmin):
    list_display = ('parking_lot', 'date', 'occupancy_rate', 'total_revenue')
    list_filter = ('parking_lot', 'date',)
    search_fields = ('parking_lot__name',)


class HourlyOccupancyAdmin(admin.ModelAdmin):
    list_display = ('parking_lot', 'date', 'hour', 'occupancy_rate')
    list_filter = ('parking_lot', 'date',)
    search_fields = ('parking_lot__name',)


# Register the models with the admin site
admin.site.register(ParkingLot, ParkingLotAdmin)
admin.site.register(ParkingTransaction, ParkingTransactionAdmin)
admin.site.register(ParkingHistory, ParkingHistoryAdmin)
admin.site.register(HourlyOccupancy, HourlyOccupancyAdmin)
