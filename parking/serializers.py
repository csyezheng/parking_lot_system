# serializers.py
from rest_framework import serializers
from .models import ParkingLot, ParkingTransaction, ParkingHistory, HourlyOccupancy, ParkingHistory


class SummarySerializer(serializers.Serializer):
    totalRevenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    totalLots = serializers.IntegerField()
    totalCapacity = serializers.IntegerField()


class RevenueLineSerializer(serializers.Serializer):
    month = serializers.CharField()
    revenue = serializers.DecimalField(max_digits=10, decimal_places=2)


class RevenueBarSerializer(serializers.ModelSerializer):
    lotName = serializers.CharField(source='parking_lot.name')

    class Meta:
        model = ParkingHistory
        fields = ['lotName', 'total_revenue']


class ParkingLotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingLot
        fields = ['id', 'name', 'capacity']


class ParkingLotDetailSerializer(serializers.Serializer):
    summary = serializers.DictField()
    historicalOccupancy = serializers.ListField()
    peakHours = serializers.ListField()
    revenueData = serializers.ListField()
    monthlyRevenueData = serializers.ListField()