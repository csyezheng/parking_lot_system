from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ParkingLotListView, SummaryView, RevenueLineView, RevenueBarView,
                    HistoricalOccupancyView, PeakHoursView, RevenueView, MonthlyRevenueView,
                    BatchImportParkingHistoryView, generate_excel_template)

urlpatterns = [
    path('summary/', SummaryView.as_view(), name='summary'),
    path('parking-lots/', ParkingLotListView.as_view(), name='parking-lot-list'),
    path('revenue-line/', RevenueLineView.as_view(), name='revenue-line'),
    path('revenue-bar/', RevenueBarView.as_view(), name='revenue-bar'),

    path('parking-lot/<int:pk>/historical-occupancy/', HistoricalOccupancyView.as_view(), name='parking-lot-historical-occupancy'),
    path('parking-lot/<int:pk>/peak-hours/', PeakHoursView.as_view(), name='parking-lot-peak-hours'),
    path('parking-lot/<int:pk>/revenue/', RevenueView.as_view(), name='parking-lot-revenue'),
    path('parking-lot/<int:pk>/monthly-revenue/', MonthlyRevenueView.as_view(), name='parking-lot-monthly-revenue'),

    path('parking-history/import/', BatchImportParkingHistoryView.as_view(), name='batch_import_parking_history'),
    path('parking-history/template/', generate_excel_template, name='generate_excel_template'),
]
