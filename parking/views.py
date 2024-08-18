# views.py
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ParkingLot, ParkingTransaction, MonthlyRevenue
from .serializers import SummarySerializer, RevenueLineSerializer, RevenueBarSerializer
from django.db.models.functions import TruncMonth


class SummaryView(APIView):
    def get(self, request):
        total_revenue = ParkingTransaction.objects.aggregate(totalRevenue=Sum('revenue'))['totalRevenue'] or 0
        total_lots = ParkingLot.objects.count()
        total_capacity = ParkingLot.objects.aggregate(totalCapacity=Sum('capacity'))['totalCapacity'] or 0

        summary_data = {
            'totalRevenue': total_revenue,
            'totalLots': total_lots,
            'totalCapacity': total_capacity,
        }
        serializer = SummarySerializer(summary_data)
        return Response(serializer.data)


class RevenueLineView(APIView):
    def get(self, request):
        # Aggregate revenue by month
        revenue_data = ParkingTransaction.objects.annotate(month=TruncMonth('entry_time')).values('month').annotate(revenue=Sum('revenue')).order_by('month')
        serializer = RevenueLineSerializer(revenue_data, many=True)
        return Response(serializer.data)


class RevenueBarView(APIView):
    def get(self, request):
        # Get the most recent month available in the MonthlyRevenue table
        latest_month_record = MonthlyRevenue.objects.order_by('-month').first()

        if not latest_month_record:
            return Response({'detail': 'No revenue data available'}, status=404)

        latest_month = latest_month_record.month

        # Filter revenue data for the latest month
        revenue_data = MonthlyRevenue.objects.filter(month=latest_month).values('parking_lot__name').annotate(total_revenue=Sum('total_revenue'))

        if not revenue_data:
            return Response({'detail': 'No revenue data available for the latest month'}, status=404)

        serializer = RevenueBarSerializer(revenue_data, many=True)
        return Response(serializer.data)
