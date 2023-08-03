import os
import sys
import traceback
# import pdfkit
from django.template.loader import render_to_string
from django.http import HttpResponse

from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings

from rest_framework.response import Response

from constants.responses import responce, success_response, failure_response
from constants import messages
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from rest_framework import status
from cm_backend.settings import *

from .models import * 
from .serializers import *

def create_space_request(request):
    with transaction.atomic():
        serializer = SpaceRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            space = serializer.validated_data.get("space")
            customer = serializer.validated_data.get("customer")
            
            # Check if an existing request already exists for the same space and customer
            existing_request = SpaceRequest.objects.filter(space=space, customer=customer,status=1)

            if existing_request.exists():
                return failure_response(status=status.HTTP_400_BAD_REQUEST, data=[], message=messages.SPACE_REQUEST_EXISTS)

            from_date = serializer.validated_data.get("valid_from")
            to_date = serializer.validated_data.get("valid_to")
            period = relativedelta(to_date, from_date)
            months = (period.years * 12) + period.months
            model_obj = serializer.save()
            model_obj.period = months
            model_obj.is_active = True
            model_obj.save()
            return success_response(status=status.HTTP_201_CREATED,message=messages.SPACE_REQUEST_CREATE_SUCCESS,data=serializer.data)

def get_space_requests(request):
    user = request.user
    role = UserRole.objects.get(user=user).role
    if role.id == 2:
        queryset = SpaceRequest.objects.filter(customer=user)
    else:
        queryset = SpaceRequest.objects.all()
    serializer =SpaceRequestSerializer(queryset,many=True)
    return success_response(status=status.HTTP_200_OK,data=serializer.data,message=messages.SPACE_REQUEST_LIST_SUCCESS)



def update_space_request_status(request,id):
    queryset = SpaceRequest.objects.get(id=id,is_active=True)
    serializer = SpaceRequestStatusUpdateSerializer(data=request.data, instance=queryset,partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    if serializer.validated_data['status'] == 2:
        msg = 'Request accepted successfully'
    if serializer.validated_data['status'] == 3:
        msg = 'Request rejected successfully'
    if serializer.validated_data['status'] == 4:
        msg = 'Request cancelled successfully'
    if serializer.validated_data['status'] == 5:
        msg = 'Security deposit initiated successfully'
    if serializer.validated_data['status'] == 6:
        msg = 'Security deposit collected'
    if serializer.validated_data['status'] == 7:
        msg = 'Request approved successfully'
    # return success_response(status=status.HTTP_200_OK,data=serializer.data,message=messages.STATUS_UPDATED)
    return success_response(status=status.HTTP_200_OK,data=serializer.data,message=msg)


# def get_contract(request):


def create_contract(request):
    data = request.data
    space = data['space']
    try:
        with transaction.atomic():
            space_obj = SpaceRequest.objects.get(id=space)

            space = space_obj.space
            period = space_obj.period
            valid_from_obj = space_obj.valid_from
            valid_to_obj = space_obj.valid_to
            rent_amount = space_obj.space.rent_price
            kiosk = space_obj.space.code
            address = space_obj.space.building.address
            electricity = space_obj.space.building.electricity_charge
            water = space_obj.space.building.water_charge
            maintenance = space_obj.space.building.maintenance_charge
            rent = space_obj.space.rent_price
            fname = space_obj.customer.first_name
            lname = space_obj.customer.last_name
            customer = space_obj.customer.id

            # print(customer)
            # print(maintenance)
            # print(electricity)
            # print(water)
            # print(rent_amount)           
            # print(period)
            # print(valid_from_obj)
            # print(valid_to_obj)
            # print(rent)

      
            contract_obj = Contract.objects.create(
                space = space,
                customer_id = customer,
                valid_from = valid_from_obj,
                valid_to = valid_to_obj,
                period = period,
                is_active = True
            )   
            contract_id = contract_obj.id

            folder_name = "contracts/contract_"+str(contract_id)+"/"
            # print(folder_name)
            # contract_path = base_path+folder_name
            path = os.path.join(MEDIA_ROOT,folder_name)
            os.mkdir(path)

            contract_obj.documentfolder = folder_name
            contract_obj.save()

            # Create the ContractDetails object
            contract_detail_obj = ContractDetails.objects.create(
                contract=contract_obj,  # Assign the contract object directly
                site_address=address,
                space_id=kiosk,
                customer=space_obj.customer.get_full_name(),
                start_date=valid_from_obj,
                end_date=valid_to_obj,
                electricity=electricity,
                water=water,
                rent_amount=rent,
                is_active = True
            )
            contract_detail_obj.save()

            space_obj.status = 7
            space_obj.save()
            space.is_available = False
            space.save()
            return success_response(status=status.HTTP_201_CREATED,message=messages.CONTRACT_CREATION_SUCCESS,data=[])
        
    except Exception as e:
        print(e)
        return failure_response(status=status.HTTP_400_BAD_REQUEST,data=contract_id,message=messages.CONTRACT_CREATION_FAILED)



def get_contract_details(request, id):
    try:
        contract = Contract.objects.get(id=id)
        contract_detail_obj = ContractDetails.objects.get(contract=contract)
        serializer = ContractDetailsSerializer(contract_detail_obj)
        return success_response(status=status.HTTP_201_CREATED,message=messages.CONTRACT_DETAILS_SUCCESS,data=serializer.data)
    except Exception as e:
        print(e)
        return failure_response(status=status.HTTP_400_BAD_REQUEST,data=[],message=messages.CONTRACT_DETAILS_FAILED)
        

# def update_contract_details(request,id):
#     with transaction.atomic():
#         try:
#             query_set = ContractDetails.objects.get(id=id)
#             print(query_set)
#             if query_set.is_active == False:
#                 return failure_response(status=status.HTTP_400_BAD_REQUEST,message=messages.CONTRACT_UPDATE_FAIL,data=[])
#             if query_set:
#                 serializer = ContractDetailsSerializer(data=request.data, instance=query_set,partial=True)
#                 print(serializer)
#                 if serializer.is_valid(raise_exception=True):
                    
                    
#                     serializer.save()
#                     return success_response(status=status.HTTP_200_OK, message=messages.CONTRACT_UPDATE_SUCCESS, data=serializer.data)
                
#                 return failure_response(status=status.HTTP_400, res_status=400)
#         except Exception as e:
#             print(e)
#             return failure_response(status=status.HTTP_400_BAD_REQUEST,data=[],message=messages.CONTRACT_FETCHING_FAIL)
    

def update_contract_details(request,id):
    with transaction.atomic():
        try:
            query_set = ContractDetails.objects.get(contract_id=id)
            serializer = ContractDetailsSerializer(data=request.data, instance=query_set,partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return success_response(status=status.HTTP_200_OK, message=messages.CONTRACT_UPDATE_SUCCESS, data=serializer.data)                
        except Exception as e:
            print(e)
            return failure_response(status=status.HTTP_400_BAD_REQUEST,data=[],message=messages.CONTRACT_UPDATE_FAILED)





# def create_contract_pdf(request):
#     data = request.data
#     contract_id = data['contract']
#     print("...", contract_id)
#     with transaction.atomic():
#         # try:
#             contract_details_obj = ContractDetails.objects.get(id=contract_id)
#             print(contract_details_obj.id)
    
#             valid_from_obj = contract_details_obj.start_date
#             print(valid_from_obj)
#             valid_to_obj = contract_details_obj.end_date
#             fname = contract_details_obj.contract.customer.first_name
#             lanme = contract_details_obj.contract.customer.last_name
#             customer = fname + ' ' + lanme
#             rent_amount = contract_details_obj.rent_amount
#             kiosk = contract_details_obj.space_id
#             address = contract_details_obj.site_address
#             electricity = contract_details_obj.electricity
#             water = contract_details_obj.water
#             clause = contract_details_obj.clause
#             period = contract_details_obj.contract.period
#             state = contract_details_obj.contract.space.building._state
#             # maintenance = space_obj.space.building.maintenance_charge
#             # print(customer)
#             # print(kiosk)
#             # print(electricity)
#             # print(water)
#             # print(rent_amount)           
#             # print(address)
#             # print(valid_from_obj)
#             # print(valid_to_obj)
#             # print(clause)

            
#             contract_details = render_to_string(os.path.join(BASE_DIR, 'templates', 'contract1.html'),
#                                         {'from':valid_from_obj, 'to': valid_to_obj, 'customer': customer, 'address':address,
#                                          'rent_amount':rent_amount, 'kiosk':kiosk, 'electricity':electricity, 'water':water,
#                                          'clause':clause, 'period':period, 'state':state})
#             html_path = os.path.join(BASE_DIR, 'templates', 'contract_details.html')
#             with open(html_path, 'w') as html_file:
#                 html_file.write(contract_details)
#             # html_path.write(bytes(contract_details, 'UTF-8'))
#                 html_file.close()

#             pdf_path = os.path.join(BASE_DIR, 'media', 'rental_agreement.pdf')

#             pdfkit.from_file(
#                 os.path.join(BASE_DIR, 'templates', 'contract_details.html'),
#                 pdf_path
#             )
#             print("valid")
#             return Response({'message': 'PDF created'})


            
def get_contract_list(request):
    contract_status = request.GET.get('status',None)
    code = request.GET.get('code',None)
    building = request.GET.get('building',None)

    user = request.user
    role = UserRole.objects.get(user=user).role
    if role.id == 2:
        queryset = Contract.objects.filter(customer=user)
    else:
        queryset = Contract.objects.all()

    
    if contract_status:
        queryset = queryset.filter(status=contract_status)
    if code:
        queryset = queryset.filter(space__code=code)
    if building:
        queryset = queryset.filter(space__building_id=building)
    serializer =ContractGetSerializer(queryset,many=True)
    return success_response(status=status.HTTP_200_OK,data=serializer.data,message=messages.CONTRACT_DETAILS_SUCCESS)

def upload_contract_documents(request):
    serializer = ContractDocumentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        contract_id = serializer.validated_data.get('contract_id')
        files= serializer.validated_data['file']
        contract_obj = Contract.objects.get(id=contract_id)
        folder_name = contract_obj.documentfolder
        path = os.path.join(MEDIA_ROOT, folder_name)
        fs = FileSystemStorage(location=path)
        for file in files:
            filename = fs.save(file.name, file)
        return success_response(status=status.HTTP_201_CREATED, message=messages.FILE_UPLOAD_SUCCESS, data=[])
