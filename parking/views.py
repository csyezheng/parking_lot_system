# views.py
import datetime
import io
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ParkingLot, ParkingTransaction, ParkingHistory
from .serializers import SummarySerializer, RevenueLineSerializer, RevenueBarSerializer
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
import openpyxl
from openpyxl.utils import get_column_letter




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
        latest_month_record = ParkingHistory.objects.order_by('-date').first()

        if not latest_month_record:
            return Response({'detail': 'No revenue data available'}, status=404)

        latest_month = latest_month_record.month

        # Filter revenue data for the latest month
        revenue_data = ParkingHistory.objects.filter(month=latest_month).values('parking_lot__name').annotate(total_revenue=Sum('total_revenue'))

        if not revenue_data:
            return Response({'detail': 'No revenue data available for the latest month'}, status=404)

        serializer = RevenueBarSerializer(revenue_data, many=True)
        return Response(serializer.data)

class BatchImportParkingHistoryView(APIView):
    def post(self, request):
        # Check if the 'file' is in request.FILES
        if 'file' not in request.FILES:
            return Response({'error': 'No file uploaded.'}, status=status.HTTP_400_BAD_REQUEST)
        file = request.FILES['file']
        try:
            workbook = openpyxl.load_workbook(io.BytesIO(file.read()))
            sheet = workbook.active

            records = []
            for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip the header row
                parking_lot_name, date_v, occupancy_rate, total_revenue = row

                try:
                    parking_lot = ParkingLot.objects.get(name=parking_lot_name)

                    # Check if date is already a datetime object
                    if isinstance(date_v, datetime.datetime):
                        date_v = date_v.date()  # Convert to date if it's a datetime
                    elif isinstance(date_v, str):
                        date_v = datetime.datetime.strptime(date_v, '%Y-%m-%d').date()

                    occupancy_rate = float(occupancy_rate) if occupancy_rate else None
                    total_revenue = float(total_revenue)

                    records.append(ParkingHistory(
                        parking_lot=parking_lot,
                        date=date_v,
                        occupancy_rate=occupancy_rate,
                        total_revenue=total_revenue
                    ))
                except ParkingLot.DoesNotExist:
                    return Response({'error': f"Parking lot {parking_lot_name} does not exist."}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            ParkingHistory.objects.bulk_create(records)
            return Response({'success': 'Data imported successfully!'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f"Error processing file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

def generate_excel_template(request):
    # Create an Excel workbook and sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Parking History Template"

    # Define the headers that match your ParkingHistory model
    headers = ["parking_lot", "date", "occupancy_rate", "total_revenue"]

    # Add headers to the first row
    for col_num, header in enumerate(headers, 1):
        col_letter = get_column_letter(col_num)
        ws[f"{col_letter}1"] = header

    # Set the content type to 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=parking_history_template.xlsx'

    # Save the workbook to the response
    wb.save(response)

    return response