from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SummaryView, RevenueLineView, RevenueBarView, BatchImportParkingHistoryView, generate_excel_template

urlpatterns = [
    path('summary/', SummaryView.as_view(), name='summary'),
    path('revenue-line/', RevenueLineView.as_view(), name='revenue-line'),
    path('revenue-bar/', RevenueBarView.as_view(), name='revenue-bar'),
    path('parking-history/import/', BatchImportParkingHistoryView.as_view(), name='batch_import_parking_history'),
    path('parking-history/template/', generate_excel_template, name='generate_excel_template'),
]