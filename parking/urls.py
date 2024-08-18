from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SummaryView, RevenueLineView, RevenueBarView

urlpatterns = [
    path('summary/', SummaryView.as_view(), name='summary'),
    path('revenue-line/', RevenueLineView.as_view(), name='revenue-line'),
    path('revenue-bar/', RevenueBarView.as_view(), name='revenue-bar'),
]