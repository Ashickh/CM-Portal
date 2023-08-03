import pytz
# from datetime import timedelta
from app.invoice_management.models import *
from app.contract_management.models import *
from app.invoice_management.serializers import *
from rest_framework import status
from constants import messages
from constants.responses import responce
import os
import sys
import traceback
import json
import requests
import pathlib
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.template.loader import render_to_string
from common.services import *
from constants.responses import *
from cm_backend.settings import *
# from app.invoice_management.serializers import UtilityReading_ApprovedSerializers,UtilityList_Serializer,InvoiceSerializer
from app.invoice_management.serializers import *
from django.core.exceptions import ValidationError
from app.user_authentication.models import *
from app.space_management.models import *
from datetime import datetime

import razorpay
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
# def utility_creation(request):


# def utility_creation(request):
#     serializer = InvoiceSerializer(data=request.data)
#     if serializer.is_valid(raise_exception = True):
#             utility = serializer.save()
#             bid=utility.space.building.id
#             sid=utility.space.id

#             electricity_folder_path = "building_"+str(bid)+"/space_"+str(sid)+"/bills/electricity/"
#             path =os.path.join(MEDIA_ROOT,electricity_folder_path)
#             fs = FileSystemStorage(location=path)
#             electricity_reading_image = request.FILES['electricity_reading_image']
#             filename = fs.save(electricity_reading_image.name,electricity_reading_image)
#             electricity_file_path = electricity_folder_path+filename

#             water_folder_path = "building_"+str(bid)+"/space_"+str(sid)+"/bills/water/"
#             path = os.path.join(MEDIA_ROOT,water_folder_path)
#             fs = FileSystemStorage(location=path)
#             water_reading_image = request.FILES['water_reading_image']
#             filename = fs.save(water_reading_image.name, water_reading_image)
#             water_file_path = water_folder_path+filename

#             utility.electricityreading_image=electricity_file_path
#             utility.waterreading_image=water_file_path
#             utility.save()

#             return success_response(status=status.HTTP_201_CREATED,message=messages.UTILITY_CREATION_SUCCESS,data=serializer.data)


def utility_creation(request):
    serializer = InvoiceSerializer(data=request.data)
    electricity_image_list = request.FILES.get('electricityreading_image')
    water_image_list = request.FILES.get('waterreading_image')

    if  UtilityReading.objects.filter(month=serializer.initial_data['month'],
        year=serializer.initial_data['year'],
        space_id=serializer.initial_data['space'],
        is_active=True).exists():
        return failure_response(status = status.HTTP_400_BAD_REQUEST,message = 'Utility reading already exist',data = '')


    if not electricity_image_list and not water_image_list:
            return failure_response(status = status.HTTP_400_BAD_REQUEST,message = 'Electricity/Water reading  image is required',data = '')

    if not electricity_image_list:
            return failure_response(status = status.HTTP_400_BAD_REQUEST,message = 'Electricity reading  image is required',data = '')
    if not water_image_list:
            return failure_response(status = status.HTTP_400_BAD_REQUEST,message = 'Water reading  image is required',data = '')
    if serializer.is_valid(raise_exception = True):
        with transaction.atomic():
            utility = serializer.save()
            bid=utility.space.building.id
            sid=utility.space.id
            electricity_folder_path = "building_"+str(bid)+"/space_"+str(sid)+"/bills/electricity/"
            path =os.path.join(MEDIA_ROOT,electricity_folder_path)
            fs = FileSystemStorage(location=path)
            electricity_image_list = request.FILES['electricityreading_image']
            filename = fs.save(electricity_image_list.name,electricity_image_list)
            electricity_folder_path = "building_"+str(bid)+"/space_"+str(sid)+"/bills/electricity/"+filename
            water_folder_path = "building_"+str(bid)+"/space_"+str(sid)+"/bills/water/"
            path = os.path.join(MEDIA_ROOT,water_folder_path)
            fs = FileSystemStorage(location=path)
            water_image_list = request.FILES['waterreading_image']
            filename = fs.save(water_image_list.name, water_image_list)
            water_folder_path = "building_"+str(bid)+"/space_"+str(sid)+"/bills/water/"+filename
            utility.electricityreading_image=electricity_folder_path
            utility.waterreading_image=water_folder_path
            utility.save()
            return success_response(status=status.HTTP_201_CREATED,message=messages.UTILITY_CREATION_SUCCESS,data=serializer.data)


def utility_edit(request,id):
    utility_reading = UtilityReading.objects.get(id=id,is_active=True)
    serializer = UtilityList_Serializer(data=request.data,instance=utility_reading,partial=True)
    if serializer.is_valid(raise_exception = True):
        with transaction.atomic():
                
                utility = serializer.save()
                bid=utility.space.building.id
                sid=utility.space.id
                

                electricity_reading_image = request.FILES.get('electricity_reading_image')

                if electricity_reading_image:

                    electricity_folder_path = "building_"+str(bid)+"/space_"+str(sid)+"/bills/electricity/"
                    path =os.path.join(MEDIA_ROOT,electricity_folder_path)
                    fs = FileSystemStorage(location=path)
                    filename = fs.save(electricity_reading_image.name, electricity_reading_image)
                    electricity_file_path = electricity_folder_path+filename
                    utility.electricityreading_image=electricity_file_path

                water_image_list = request.FILES.get('water_reading_image')

                if water_image_list:
                    water_folder_path = "building_"+str(bid)+"/space_"+str(sid)+"/bills/water/"
                    path = os.path.join(MEDIA_ROOT,water_folder_path)
                    fs = FileSystemStorage(location=path)
                    filename = fs.save(water_image_list.name, water_image_list)
                    water_file_path = water_folder_path+filename
                    utility.waterreading_image=water_file_path

                if 'deleted_images_electricityreading' in request.data:
                    deleted_images_electricityreading = request.data['deleted_images_electricityreading']
                    imgpath = os.path.join(BASE_DIR,deleted_images_electricityreading)
                    print(imgpath)

                    if os.path.isfile(imgpath):
                            os.remove(imgpath)
                    # if os.path.exists(deleted_images_electricityreading):
                    #     os.remove(deleted_images_electricityreading)


                # water_folder_path = "building_"+str(bid)+"/space_"+str(sid)+"/bills/water"
                # path = os.path.join(MEDIA_ROOT,water_folder_path)
                # fs = FileSystemStorage(location=path)
                # water_image_list = request.FILES['water_reading_image']
                # filename = fs.save(water_image_list.name, water_image_list)
                # water_file_path = water_folder_path+filename

                if 'deleted_images_waterreading' in request.data:
                    deleted_images_waterreading = request.data['deleted_images_waterreading']
                    # if os.path.exists(deleted_images_waterreading):
                    #    os.remove(deleted_images_waterreading)

                    imgpath = os.path.join(BASE_DIR,deleted_images_waterreading)
                    print(imgpath)

                    if os.path.isfile(imgpath):
                            os.remove(imgpath)

                # utility.electricityreading_image=electricity_file_path
                # utility.waterreading_image=water_file_path
                utility.save()
                return success_response(status=status.HTTP_200_OK, message=messages.UTILITY_UPDATE_SUCCESS, data=serializer.data)




def utilityreading_delete(request,id):
    utility = UtilityReading.objects.get(id=id,is_active=True)
    with transaction.atomic():
        utility.is_active = False
        utility.save()
        return success_response(status = status.HTTP_200_OK,message = messages.UTILITY_DELETE_SUCESS,data = '')

def utilityreading_get(request):
    queryset=UtilityReading.objects.filter(is_active=True)
    month = request.GET.get('month')
    year = request.GET.get('year')
    space = request.GET.get('space')
    building = request.GET.get('building')

    if month:
        queryset = queryset.filter(month=month)
    if year:
        queryset = queryset.filter(year=year)
    if space:
        queryset = queryset.filter(space=space)    
    if building:
        queryset = queryset.filter(space__building_id=building)
    serializer=UtilityList_Serializer(queryset,many=True)   
    return success_response(status = status.HTTP_200_OK,message = messages.UTILITY_DETAILS_FETCH_SUCCESS,data = serializer.data)

#for finance team        
def utility_approval(request,id):
        utility_reading = UtilityReading.objects.get(id=id)
        serializer = InvoiceSerializer(instance=utility_reading, data=request.data, partial=True)
        if serializer.is_valid():
            utility=serializer.save()
            utility.is_approved=True
            utility.save()
            return success_response(status=status.HTTP_200_OK, message=messages.UTILITY_APPROVED_SUCCESS, data=[])

# grievances services
def grievances_creation(request):
    serializer = GrievancesSerializer(data=request.data,context={'request':request})
    if serializer.is_valid(raise_exception = True):
        with transaction.atomic():
            grievances = serializer.save()
            grievances.is_active=True
            grievances.save()
            return success_response(status=status.HTTP_201_CREATED,message=messages.CREATION_SUCCESS,data=serializer.data)

def grievances_assigning(request,id):
    grievance = Grievances.objects.get(id=id,is_active=True)
    serializer = GrievancesAssigningSerializer(instance=grievance, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        with transaction.atomic():
            grievances=serializer.save()
            return success_response(status=status.HTTP_200_OK, message=messages.GRIVANCE_ASSIGN_SUCCESS, data=[])

def change_grievances_status(request,id):
    grievance = Grievances.objects.get(id=id,is_active=True)
    serializer = ChangeGrievancesStatusSerializer(instance=grievance, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        with transaction.atomic():
            grievances=serializer.save()
            if serializer.validated_data['issue_status'] == 3:
                msg = messages.GRIVANCE_IN_PROGRESS_SUCCESS
            if serializer.validated_data['issue_status'] == 4:
                msg = messages.GRIVANCE_CLOSED_SUCCESS
            if serializer.validated_data['issue_status'] == 5:
                msg = messages.GRIVANCE_DECLINED_SUCCESS
            return success_response(status=status.HTTP_200_OK, message=msg, data=[])

def grievances_list(request):
   issue_type = request.GET.get('issue_type')
   current_user=request.user
   role = UserRole.objects.get(user=current_user,is_active=True).role
   if role.id == 1:
        queryset = Grievances.objects.filter(is_active=True)
   elif role.id == 2:
        queryset = Grievances.objects.filter(customer=current_user,is_active=True)
   else:
        queryset = Grievances.objects.filter(assignee=request.user,is_active=True)
   if issue_type:
        queryset = queryset.filter(issue_type=issue_type)
   serializer=GrievancesListSerializer(queryset,many=True)
   return success_response(status = status.HTTP_200_OK,message = messages.DETAIL_FETCH_SUCCESS,data = serializer.data)

def grievances_track(request,id):
    grievance = Grievances.objects.get(id=id,is_active=True)
    serializer=GrievanceDetailSerializer(grievance)
    return success_response(status = status.HTTP_200_OK,message = messages.DETAIL_FETCH_SUCCESS,data = serializer.data)

def grievances_delete(request,id):
    grievance = Grievances.objects.get(id=id,is_active=True)
    with transaction.atomic():
        grievance.is_active =False
        grievance.save()
        return success_response(status = status.HTTP_200_OK,message = messages.DELETION_SUCCESS,data = [])

# for bill 
def get_bill_by_date(request):
    try:
        user = request.user
        print(user)
        print("inside bill method")
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        building = request.GET.get('building',None)
        space = request.GET.get('space',None)
        tz = pytz.timezone('UTC')  # Replace 'YOUR_TIMEZONE' with the appropriate time zone
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').replace(tzinfo=tz)
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').replace(tzinfo=tz)
        print(start_date)
        print(end_date)

        role = UserRole.objects.get(user=user,is_active=True).role
        if role.id == 2:
            queryset =Invoice.objects.filter(customer=user,is_created__range=(start_date, end_date),is_active=True)
        else:
            queryset =Invoice.objects.filter(is_created__range=(start_date, end_date),is_active=True)
        if building:
            queryset = queryset.filter(space__building=building)
        if space:
            queryset = queryset.filter(space=space)

        serializer = BillListSerializer(queryset,many=True)

        return success_response(status=status.HTTP_201_CREATED,message=messages.DETAIL_FETCH_SUCCESS,data=serializer.data)

    except Exception as e:
        print(e)
        return failure_response(status=status.HTTP_400_BAD_REQUEST,data=[],message=messages.DETAIL_FETCH_FAIL)
        
# for invoices
def invoice_generation(request):
    try:
        user = request.user
        month = request.GET.get('month')
        year = request.GET.get('year')
        date_type = request.GET.get('type')
        q_type = request.GET.get('quarter')
        
        if date_type == 'Monthly':

            role = UserRole.objects.get(user=user,is_active=True).role
            if role.id == 2:
                queryset =Invoice.objects.filter(customer=user,month=month,year=year,is_active=True)
            else:
                queryset =Invoice.objects.filter(month=month,year=year,is_active=True)

            serializer = BillListSerializer(queryset,many=True)

            return success_response(status=status.HTTP_201_CREATED,message=messages.DETAIL_FETCH_SUCCESS,data=serializer.data)
        
        if date_type == 'Quarterly':
            if q_type == 'Q1':
                month_list = [1,2,3]
            elif q_type == 'Q2':
                month_list = [4,5,6]
            elif q_type == 'Q3':
                month_list = [7,8,9]
            elif q_type == 'Q4':
                month_list = [10,11,12]

            if role.id == 2:
                queryset =Invoice.objects.filter(customer=user,month__in=month_list,year=year,is_active=True)
            else:
                queryset =Invoice.objects.filter(month__in=month_list,year=year,is_active=True)

            distinct_customer_spaces = queryset.distinct('space','customer')
            serializer = InvoiceListSerializer(distinct_customer_spaces,many=True,context={'queryset':queryset})

            return success_response(status=status.HTTP_201_CREATED,message=messages.DETAIL_FETCH_SUCCESS,data=serializer.data)

    except Exception as e:
        print(e)
        return failure_response(status=status.HTTP_400_BAD_REQUEST,data=[],message=messages.DETAIL_FETCH_FAIL)

def alert_messages(request):
    pending_invoices = Invoice.objects.filter(payment_status=1,is_active=True)
    current_date = datetime.datetime.now().date()
    messages_to_send = []
    for invoice in pending_invoices:
        due_date = invoice.due_date
        five_days_before = due_date - timedelta(days=5)
        three_days_before = due_date - timedelta(days=3)
        one_day_before = due_date - timedelta(days=1)
        msg =f"Hi {invoice.customer.first_name}, This is just a reminder that rent is due on {invoice.due_date}. So, please be sure to make your payment on time to avoid any late fees. Thanks!"
        msg1 = f"Hi {invoice.customer.first_name} , Given that the invoice is now past the due date, a late payment fee of ₹100 has been applied to the bill. Kindly make the payment at the earliest. Thanks!"
        if current_date == five_days_before:
            messages_to_send.append({"message": msg,"color_code": "Green"})
        elif current_date == three_days_before:
            messages_to_send.append({"message": msg,"color_code": "Yellow"})
        elif current_date == one_day_before:
            messages_to_send.append({"message": msg,"color_code": "Red"})
        elif current_date >= invoice.due_date:
            messages_to_send.append({"message": msg1})
    return success_response(status=status.HTTP_200_OK,message=messages.DETAIL_FETCH_SUCCESS,data=messages_to_send)


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def security_deposit_payment(request):

    request_id = request.GET.get('request_id')
    space_obj = SpaceRequest.objects.get(id=request_id)

    currency = 'INR'
    amount_obj = space_obj.space.security_deposit
    amount = amount_obj * 100
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(
        dict(
            amount=amount,
            currency=currency,
            payment_capture='0',
            notes={'space_id': request_id}
        )
    )
    # Extract the order ID from the Razorpay order object
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'       
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZORPAY_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    # return render(request, 'index.html', context=context)    
    # return Response(status=status.HTTP_201_CREATED, data=context, message='')
    return success_response(status=status.HTTP_200_OK,message=messages.DETAIL_FETCH_SUCCESS,data=context)


# @csrf_exempt
def paymenthandler(request):

    # Only accept POST request.
    if request.method == "POST":
        try:
            # Get the required parameters from the POST request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            print(payment_id)
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            order = razorpay_client.order.fetch(razorpay_order_id)
            order_amount = order['amount']
            print(order_amount)
            space_id = order['notes']['space_id']
            print(space_id)
            signature = request.POST.get('razorpay_signature', '')
            
            # Verify the payment signature.
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            print(result)
            if result is not None:
                amount = order_amount  # Replace with the actual amount to capture
                print(amount)
                try:
                    # Capture the payment
                    response = razorpay_client.payment.capture(payment_id, amount)
                    print("response is:" ,response)
                    
                    if response:
                        try:
                            pay_id = response['id']                       
                            order_id = response['order_id']                           
                            paid_amount = response['amount']
                            actual_amount = paid_amount/100                        
                            currency = response['currency']                        
                            status = response['status']                           
                            created_at = response['created_at']
                            created_at_datetime = datetime.fromtimestamp(created_at, pytz.UTC)                       
                            error_code = response['error_code'] 
                            rrn = response['acquirer_data']['rrn']

                            payment_data = {
                                            'payment_id':pay_id, 
                                            'order_id':order_id, 
                                            'currency':currency,
                                            'amount':actual_amount, 
                                            'status':status, 
                                            'created_at':created_at_datetime,
                                            'error_code':error_code
                                            }
                            print(payment_data)
                            payment_obj = Payment.objects.create(**payment_data)
                            payment_obj.save() 
                            print(payment_obj)                          
                        except Exception as e:
                            print(e)                   
                    if response['status'] == 'captured':
                        try:
                            space_obj = SpaceRequest.objects.get(id=space_id)
                            print(space_obj)
                            space_obj.security_payment = payment_obj
                            space_obj.save()
                            print("Security Payment updated successfully")                           
                        except Invoice.DoesNotExist:
                            print("Space not found")
                    else:
                        print("Payment capture was unsuccessful")
                    
                    #  we need to pass these details to frontend.
                    context = {}
                    context['reference'] = pay_id
                    context['reference'] = rrn
                    context['payment_created'] = created_at_datetime
                    context['Paid_amount'] = actual_amount
                    context['currency'] = currency

                    # context = {
                    #             'reference': pay_id,
                    #             'rrn': rrn,
                    #             'payment_created': created_at_datetime,
                    #             'Paid_amount': actual_amount,
                    #             'currency': currency
                    #         }
                    # return JsonResponse(context)
                
                    # google_url = 'http://rental.pearlglobalsolutions.com/login'
                    # query_params = {'reference': pay_id, 'payment_created': created_at_datetime, 'Paid_amount':actual_amount}  
                    # return redirect(f"{google_url}?{urlencode(query_params)}")
                    
                # else:
                #     return JsonResponse({'message': 'Payment capture was unsuccessful'})

                    # Render the success page on successful capture of payment
                    return render(request, 'security_paymentsuccess.html', context=context)
                except:
                    # If there is an error while capturing payment
                    return render(request, 'paymesecurity_paymentntfail.html')
            else:
                # If signature verification fails
                return render(request, 'security_payment.html')
        except:
            # If the required parameters are not found in the POST data
            return HttpResponseBadRequest()
    else:
        # If a method other than POST is used
        return HttpResponseBadRequest()


def create_notification(request):
  
    serializer = Notification_ContentSerializer(data=request.data)
    if serializer.is_valid(raise_exception = True):
        with transaction.atomic():
            notification = serializer.save()
            notification.is_active=True
            notification.save()
            return success_response(status=status.HTTP_201_CREATED,message=messages.CREATION_SUCCESS,data=serializer.data)
        
def get_notifications(request):
    notification_obj  = Notification_Content.objects.all()
    serializer = Notification_ContentSerializer(notification_obj, many=True)
    return success_response(status=status.HTTP_200_OK,data=serializer.data,message=messages.DETAIL_FETCH_SUCCESS)
