from genericpath import exists
from app.contract_management.models import *
from app.invoice_management.models import *
from app.invoice_management.serializers import *
from rest_framework import status
from constants import messages
from common.services import *
from constants.responses import *
from app.report_management.serializers import *
from django.db.models import F


def get_customerdetails(request):
    month = request.GET.get('month',None)
    year = request.GET.get('year',None)
    building = request.GET.get('building',None)
    user = request.user
    role = UserRole.objects.get(user=user).role
    if role.id == 2:
        queryset = Invoice.objects.filter(customer=user,payment_status=2)
    else:
        queryset = Invoice.objects.filter(payment_status=2)

    if month:
        queryset = queryset.filter(month=month)
    if year:
        queryset = queryset.filter(year=year)
    if building:
        queryset = queryset.filter(space__building_id=building)
    serializer =CustomerReportSerializer(queryset,many=True)
    return success_response(status=status.HTTP_200_OK,message=messages.REPORT_FETCH_SUCCESS,data=serializer.data)


def get_revenuedetails(request):
    building = request.GET.get('building',None)
    month = request.GET.get('month',None)
    year = request.GET.get('year',None)
    period_type = request.GET.get('type',None)
    period = request.GET.get('period',None)
    user = request.user
    role = UserRole.objects.get(user=user).role
    if role.id == 2:
        queryset = Invoice.objects.filter(customer=user,payment_status=2)
    else:
        queryset = Invoice.objects.filter(payment_status=2)
        
    if building:
        queryset = queryset.filter(space__building_id=building)
    if period_type == 'Monthly':
        if month and year:
            queryset = queryset.filter(invoice_date__month=month, invoice_date__year=year)
        else:
            return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
    elif period_type == 'Quarterly':
        if period and year:
            if period == 'Q1':
                queryset = queryset.filter(invoice_date__month__in=[1, 2, 3], invoice_date__year=year)
            elif period == 'Q2':
                queryset = queryset.filter(invoice_date__month__in=[4, 5, 6], invoice_date__year=year)
            elif period == 'Q3':
                queryset = queryset.filter(invoice_date__month__in=[7, 8, 9], invoice_date__year=year)
            elif period == 'Q4':
                queryset = queryset.filter(invoice_date__month__in=[10, 11, 12], invoice_date__year=year)
            else:
                return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
        else:
            return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
    elif period_type == 'HalfYearly':
        if period and year:
            if period == 'H1':
                queryset = queryset.filter(invoice_date__month__in=[1, 2, 3, 4, 5, 6],invoice_date__year=year)
            elif period == 'H2':
                queryset = queryset.filter(invoice_date__month__in=[7, 8, 9, 10, 11, 12],invoice_date__year=year)
            else:
                return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
        else:
            return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
    elif period_type == 'Yearly':
        if year:
            queryset = queryset.filter(invoice_date__year=year)
        else:
            return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
   
    if not queryset.exists():
        return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
    
    serializer = RevenueReportSerializer(queryset, many=True)
    return success_response(status=status.HTTP_200_OK, message=messages.REPORT_FETCH_SUCCESS, data=serializer.data)

    




def get_building_revenuedetails(request):
    building = request.GET.get('building',None)
    month = request.GET.get('month',None)
    year = request.GET.get('year',None)
    period_type = request.GET.get('type',None)
    period = request.GET.get('period',None)
    user = request.user
    role = UserRole.objects.get(user=user).role
    if role.id == 2:
        queryset = Invoice.objects.filter(customer=user,payment_status=2)
    else:
        queryset = Invoice.objects.filter(payment_status=2)
    
    if building:
        queryset = queryset.filter(space__building_id=building)

    if period_type == 'Monthly':
        if month and year:
            queryset = queryset.filter(invoice_date__month=month, invoice_date__year=year)
        else:
            return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
    elif period_type == 'Quarterly':
        if period and year:
            if period == 'Q1':
                queryset = queryset.filter(invoice_date__month__in=[1, 2, 3], invoice_date__year=year)
            elif period == 'Q2':
                queryset = queryset.filter(invoice_date__month__in=[4, 5, 6], invoice_date__year=year)
            elif period == 'Q3':
                queryset = queryset.filter(invoice_date__month__in=[7, 8, 9], invoice_date__year=year)
            elif period == 'Q4':
                queryset = queryset.filter(invoice_date__month__in=[10, 11, 12], invoice_date__year=year)
            else:
                return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
        else:
            return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
    elif period_type == 'HalfYearly':
        if period and year:
            if period == 'H1':
                queryset = queryset.filter(invoice_date__month__in=[1, 2, 3, 4, 5, 6], invoice_date__year=year)
            elif period == 'H2':
                queryset = queryset.filter(invoice_date__month__in=[7, 8, 9, 10, 11, 12], invoice_date__year=year)
            else:
                return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
        else:
            return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
    elif period_type == 'Yearly':
        if year:
            queryset = queryset.filter(invoice_date__year=year)
        else:
            return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
    
    if not queryset.exists():
        return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)

    queryset=(queryset.values('space__building').annotate(total_revenue=Sum('rent_amount')))
    serializer = BuildingRevenueReportSerializer(queryset,many=True)
    return success_response(status=status.HTTP_200_OK, message=messages.REPORT_FETCH_SUCCESS, data=serializer.data)

def get_amount_deposited_details(request):
    user = request.user
    role = UserRole.objects.get(user=user).role
    if role.id == 2:
        queryset = SpaceRequest.objects.filter(customer=user,security_payment__status='captured')
    else:
        queryset = SpaceRequest.objects.filter(security_payment__status='captured')
    serializer = AmountDepositedReportSerializer(queryset, many=True)
    return success_response(status=status.HTTP_200_OK, message=messages.REPORT_FETCH_SUCCESS, data=serializer.data)


def get_salesdetails(request):
    user = request.user
    building = request.GET.get('building',None)
    month = request.GET.get('month',None)
    year = request.GET.get('year',None)
    period_type = request.GET.get('type',None)
    period = request.GET.get('period',None)
    role = UserRole.objects.get(user=user).role
    if role.id == 2:

        query_set = Invoice.objects.filter(payment_status=2,customer=user)
        queryset = query_set.filter(space__is_available=False)
    else:
        query_set = Invoice.objects.filter(payment_status=2)
        queryset = query_set.filter(is_active=True)

    if building:
        queryset = queryset.filter(space__building_id=building)
        print(queryset)
    if period_type == 'Monthly':
        if month and year:
            queryset = queryset.filter(invoice_date__month=month,invoice_date__year=year)
        else:
            return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
    elif period_type == 'Quarterly':
        if period and year:
            if period == 'Q1':
                queryset = queryset.filter(invoice_date__month__in=[1, 2, 3], invoice_date__year=year)
            elif period == 'Q2':
                queryset = queryset.filter(invoice_date__month__in=[4, 5, 6], invoice_date__year=year)
            elif period == 'Q3':
                queryset = queryset.filter(invoice_date__month__in=[7, 8, 9], invoice_date__year=year)
            elif period == 'Q4':
                queryset = queryset.filter(invoice_date__month__in=[10, 11, 12], invoice_date__year=year)
            else:
                return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
        else:
            return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
    elif period_type == 'HalfYearly':
        if period and year:
            if period == 'H1':
                queryset = queryset.filter(invoice_date__month__in=[1, 2, 3, 4, 5, 6], invoice_date__year=year)
            elif period == 'H2':
                queryset = queryset.filter(invoice_date__month__in=[7, 8, 9, 10, 11, 12], invoice_date__year=year)
            else:
                return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
        else:
            return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
    elif period_type == 'Yearly':
        if year:
            queryset = queryset.filter(invoice_date__year=year)
        else:
            return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)

    if not queryset.exists():
        return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)

    serializer = SalesReportSerializer(queryset, many=True)
    if not queryset.exists():
        return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
    queryset = (
            queryset.values('space__building').annotate(total_space=Count('id'),total_rent=Sum('rent_amount'))
        ) 
    serializer = SalesReportSerializer(queryset,many=True)     
    return success_response(status=status.HTTP_200_OK, message=messages.REPORT_FETCH_SUCCESS, data=serializer.data)

def get_document_details(request):
        building = request.GET.get('building',None)
        month = request.GET.get('month',None)
        year = request.GET.get('year',None)
        period_type = request.GET.get('type',None)
        period = request.GET.get('period',None)
        user = request.user
        role = UserRole.objects.get(user=user).role
        if role.id == 2:
            queryset = Contract.objects.filter(is_active=True,customer=user)
        else:
            queryset = Contract.objects.filter(is_active=True)

        serializer = DocumentReportSerializer(queryset, many=True)
        if not queryset.exists():
             return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.REPORT_FETCH_FAIL)
        return success_response(status=status.HTTP_200_OK, message=messages.REPORT_FETCH_SUCCESS, data=serializer.data)