from django.urls import path
from .views import * 

urlpatterns = [
    path("rentpaid/",CustomerReportView.as_view()),
    path("revenue/",RevenueReportView.as_view()),
    path("building_revenue/",BuildingRevenueReportView.as_view()),
    path("amount_deposited/",AmountDepositedReportView.as_view()),
    path('sales_report/',SalesRportView.as_view()),
    path('document_report/',DocumentReportView.as_view()),
   
    
]
