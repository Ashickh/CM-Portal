from django.shortcuts import render
from rest_framework.views import APIView
from app.report_management.services import *
from rest_framework import generics, permissions
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
# Create your views here.


class CustomerReportView(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    def get(self,request):
        return get_customerdetails(request=request)
class RevenueReportView(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    def get(self,request):
        return get_revenuedetails(request=request)

class BuildingRevenueReportView(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    def get(self,request):
        return get_building_revenuedetails(request=request)

class AmountDepositedReportView(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    def get(self,request):
        return get_amount_deposited_details(request=request)

class SalesRportView(APIView):
    permission_classes = [permissions.IsAuthenticated,TokenHasReadWriteScope]
    def get(self, request):
        return get_salesdetails(request=request)

class DocumentReportView(APIView):
    permission_classes = [permissions.IsAuthenticated,TokenHasReadWriteScope]
    def get(self, request):
        return get_document_details(request=request)        