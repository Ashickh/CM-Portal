from django.shortcuts import render
from rest_framework.views import APIView

from app.invoice_management import services
from app.invoice_management.services import *

from rest_framework import generics
from app.invoice_management.models import *
from app.invoice_management.serializers import *

from rest_framework import generics, permissions
from .services import *
from app.invoice_management.custom_permissions  import *
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

# Create your views here.
class UtilityView(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope, UtilityPermission]

    def post(self, request):
        return utility_creation(request=request)

    def get(self,request):
        return utilityreading_get(request=request)    


class UtilityEditView(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope, UtilityPermission]

    def put(self, request,id):
        return utility_edit(request=request, id=id)   

    def delete(self,request,id):
        return utilityreading_delete(request=request, id=id)    


class UtilityReading_ApprovingView(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope, UtilityPermission]
    
    def put(self,request,id):
        return utility_approval(request=request, id=id)
    

#grievances
class GrievancesView(APIView):

    permission_classes = [permissions.IsAuthenticated,TokenHasReadWriteScope,GrievancesPermission]

    def post(self, request):
        return grievances_creation(request=request)

    def get(self,request):
        return grievances_list(request=request) 

# class GrievancesAssigningView(APIView):

#     permission_classes = [permissions.IsAuthenticated,TokenHasReadWriteScope,GrievancesPermission]

#     def put(self,request,id):
#         return grievances_assigning(request=request,id=id)


class GrievancesStatusUpdateView(APIView):

    permission_classes = [permissions.IsAuthenticated,TokenHasReadWriteScope,GrievancesPermission]

    def put(self,request,id):
        return change_grievances_status(request=request,id=id)

class GrievancesDetailView(APIView):

    permission_classes = [permissions.IsAuthenticated,TokenHasReadWriteScope,GrievancesPermission]

    def get(self,request,id):
        return grievances_track(request=request,id=id)    
           
    def delete(self,request,id):
        return grievances_delete(request=request, id=id)       
        
    def put(self,request,id):
        return grievances_assigning(request=request,id=id)


class BillFilterView(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    def get(self, request):
        return get_bill_by_date(request=request)


class InvoiceFilterView(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    def get(self, request):
        return invoice_generation(request=request)


class SendAlertMessagesView(APIView):
    def get(self,request):
        return alert_messages(request=request)


class SecurityPaymentView(APIView):
    def get(self,request):
        return security_deposit_payment(request=request)
    
    
class SecurityPaymentCallbackView(APIView):
    def post(self,request):
        return paymenthandler(request=request)
    
class NotificationContent(APIView):
    def get(self, request):
        return get_notifications(request=request)

    def post(self, request):
        return create_notification(request=request)