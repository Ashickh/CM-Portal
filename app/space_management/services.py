import os
import sys
import traceback
import json
import requests
import pathlib

from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.template.loader import render_to_string
from rest_framework import status

from common.services import *
from constants import messages
from constants.responses import *
from cm_backend.settings import *
from app.space_management.serializers import *
from app.space_management.models import *


def get_all_country(request):
    queryset = Country.objects.filter(is_active=True)
    serializer = CountrySerializer(queryset,many=True)    
    return success_response(status=status.HTTP_200_OK,message='',data=serializer.data)
 
def get_all_states(request):
    country_id = request.GET.get('country_id',None)
    queryset = State.objects.filter(country__id=country_id,is_active=True)
    serializer = StateSerializer(queryset,many=True)    
    return success_response(status=status.HTTP_200_OK,message='',data=serializer.data)

def get_all_cities(request):
    state_id = request.GET.get('state_id',None)
    queryset = City.objects.filter(state__id=state_id,is_active=True)
    serializer = CitySerializer(queryset,many=True)    
    return success_response(status=status.HTTP_200_OK,message='',data=serializer.data)

def get_city_details(request,id):
    city = City.objects.get(id=id,is_active=True)
    serializer = CitySerializer(city)    
    return success_response(status=status.HTTP_200_OK,message='',data=serializer.data)


def add_new_city(request):
    serializer = CitySerializer(data=request.data)
    if serializer.is_valid(raise_exception = True):
        if City.objects.filter(name=serializer.validated_data['name'],is_active=True).exists():
            return failure_response(status=status.HTTP_400_BAD_REQUEST,message=messages.DUPLICATE_CITY_EXIST,data='')
        else:
            with transaction.atomic():
                city = serializer.save()
                city.is_active=True
                city.save()
                return success_response(status=status.HTTP_201_CREATED,message=messages.CITY_CREATION_SUCESS,data=serializer.data)

def update_city(request,id):
    city_obj = City.objects.get(id=id,is_active=True)
    serializer = CitySerializer(data=request.data, instance=city_obj,partial=True)
    if serializer.is_valid(raise_exception = True):
        name = serializer.validated_data['name']
        if City.objects.filter(name=name,is_active=True).exclude(id=id).exists():
            return failure_response(status=status.HTTP_400_BAD_REQUEST,message=messages.DUPLICATE_CITY_EXIST,data='')
        else:
            with transaction.atomic():
                serializer.save()
                return success_response(status = status.HTTP_200_OK,message = messages.CITY_UPDATE_SUCESS,data = '')

def delete_city(request,id):
    city = City.objects.get(id=id,is_active=True)
    with transaction.atomic():
        city.is_active = False
        city.save()
        Building.objects.filter(city=city,is_active=True).update(is_active=False)
        return success_response(status = status.HTTP_200_OK,message = messages.CITY_DELETE_SUCESS,data = '')

def add_new_building(request):
    serializer = BuildingSerializer(data=request.data)
    if serializer.is_valid(raise_exception = True):
        if Building.objects.filter(name=serializer.validated_data['name'],is_active=True).exists():
            return failure_response(status=status.HTTP_400_BAD_REQUEST,message=messages.DUPLICATE_BUILDING_EXIST,data='')
        else:
            with transaction.atomic():
                building = serializer.save()

                path = os.path.join(MEDIA_ROOT,building.image_folder)
                fs = FileSystemStorage(location=path)
                image_list = request.FILES.getlist('image_list')
                for img in image_list:
                    filename = fs.save(img.name, img)

                return success_response(status=status.HTTP_201_CREATED,message=messages.BUILDING_CREATION_SUCESS,data=serializer.data)

def get_each_building(request,id):
    building = Building.objects.get(id=id,is_active=True)
    serializer = BuildingSerializer(building)

    folder = building.image_folder
    path = os.path.join(MEDIA_ROOT,folder)
    arr = os.listdir(path)
    arr = [f.name for f in pathlib.Path(path).iterdir() if f.is_file()]
    for index,item in enumerate(arr):
        arr[index] = MEDIA_URL+folder+item

    building_data = {"building_data":serializer.data,"imguls":arr}

    return success_response(status=status.HTTP_201_CREATED,message=messages.BUILDING_DETAILS_FETCH_SUCCESS,data=building_data) 

def update_building(request,id):
    building_obj = Building.objects.get(id=id,is_active=True)
    serializer = BuildingSerializer(data=request.data, instance=building_obj,partial=True)
    if serializer.is_valid(raise_exception = True):

        name = serializer.validated_data['name']
        if Building.objects.filter(name=name,is_active=True).exclude(id=id).exists():
            return failure_response(status=status.HTTP_400_BAD_REQUEST,message=messages.DUPLICATE_BUILDING_EXIST,data='')
        else:
            with transaction.atomic():
                building = serializer.save()

                path = os.path.join(MEDIA_ROOT,building.image_folder)
                fs = FileSystemStorage(location=path)
                image_list = request.FILES.getlist('image_list')
                for img in image_list:
                    filename = fs.save(img.name, img)

                if 'deleted_images' in request.data:
                    deleted_images = request.data['deleted_images']
                    for url in deleted_images:
                        print(url)
                        imgpath = os.path.join(BASE_DIR,url)
                        print(imgpath)
                        if os.path.isfile(imgpath):
                            os.remove(imgpath)

                return success_response(status = status.HTTP_200_OK,message = messages.BUILDING_UPDATE_SUCESS,data = '')

def delete_building(request,id):
    building = Building.objects.get(id=id,is_active=True)
    with transaction.atomic():
        building.is_active = False
        building.save()
        RentalSpace.objects.filter(building=building,is_active=True).update(is_active=False)
        return success_response(status = status.HTTP_200_OK,message = messages.BUILDING_DELETE_SUCESS,data = '')

def get_building(request):
    queryset = Building.objects.filter(is_active=True)
    serializer = BuildingSerializer(queryset,many=True)    
    return success_response(status=status.HTTP_200_OK,message='',data=serializer.data)
 
def add_new_space(request):
    serializer = RentalSpaceSerializer(data=request.data,context={'request':request})
    if serializer.is_valid(raise_exception = True):
        if RentalSpace.objects.filter(code__iexact=serializer.validated_data['code'],is_active=True).exists():
            return failure_response(status=status.HTTP_400_BAD_REQUEST,message=messages.SPACE_DUPLICATE_EXIST,data='')
        else:
            space = serializer.save()

            path = os.path.join(MEDIA_ROOT,space.image_folder)
            fs = FileSystemStorage(location=path)
            image_list = request.FILES.getlist('image_list')
            for img in image_list:
                filename = fs.save(img.name, img)

            path = os.path.join(MEDIA_ROOT,space.document_folder)
            fs = FileSystemStorage(location=path)
            document_list = request.FILES.getlist('document_list')
            for doc in document_list:
                filename = fs.save(doc.name, doc)

            return success_response(status=status.HTTP_201_CREATED,message=messages.SPACE_CREATION_SUCESS,data=serializer.data)


def get_space_details(request,id):
    space = RentalSpace.objects.get(id=id,is_active=True)
    serializer = RentalSpaceSerializer(space,context={'request':request})
    print(serializer.data)
    image_folder = space.image_folder
    document_folder = space.document_folder
    path = os.path.join(MEDIA_ROOT,image_folder)
    arr = os.listdir(path)
    arr = [f.name for f in pathlib.Path(path).iterdir() if f.is_file()]
    print(arr)
    for index,item in enumerate(arr):
        arr[index] = MEDIA_URL+image_folder+item
        # print(path,item,arr[index])
        # print(API_URL+MEDIA_URL+folder+item)
    image_urls = arr

    path = os.path.join(MEDIA_ROOT,document_folder)
    arr = os.listdir(path)
    arr = [f.name for f in pathlib.Path(path).iterdir() if f.is_file()]
    print(arr)
    for index,item in enumerate(arr):
        arr[index] = MEDIA_URL+document_folder+item
        # print(path,item,arr[index])
        # print(API_URL+MEDIA_URL+folder+item)
    document_urls = arr


    space_data = {"building_data":serializer.data,"image_urls":image_urls,"document_urls":document_urls}
    return success_response(status=status.HTTP_201_CREATED,message=messages.SPACE_DETAILS_FETCH_SUCCESS,data=space_data) 


def delete_space(request,id):
    space = RentalSpace.objects.get(id=id,is_active=True)
    with transaction.atomic():
        space.is_active = False
        space.save()
        return success_response(status = status.HTTP_200_OK,message = messages.SPACE_DELETE_SUCESS,data = '')


def get_spaces(request):
    building_id = request.GET.get('building_id',None)
    queryset = RentalSpace.objects.filter(is_active=True,building__is_active=True)
    if building_id:
        queryset =queryset.filter(building_id=building_id)
    serializer = RentalSpaceSerializer(queryset,many=True,context={'request':request})    
    return success_response(status=status.HTTP_200_OK,message='',data=serializer.data)


def update_space(request,id):
    space_obj = RentalSpace.objects.get(id=id,is_active=True)
    serializer = RentalSpaceSerializer(data=request.data, instance=space_obj,partial=True,context={'request':request})
    if serializer.is_valid(raise_exception = True):

        code = serializer.validated_data['code']
        if RentalSpace.objects.filter(code__iexact=code,is_active=True).exclude(id=id).exists():
            return failure_response(status=status.HTTP_400_BAD_REQUEST,message=messages.SPACE_DUPLICATE_EXIST,data='')
        else:
            with transaction.atomic():
                space = serializer.save()

                path = os.path.join(MEDIA_ROOT,space.image_folder)
                fs = FileSystemStorage(location=path)
                image_list = request.FILES.getlist('image_list')
                for img in image_list:
                    filename = fs.save(img.name, img)

                if 'deleted_images' in request.data:
                    deleted_images = request.data['deleted_images']
                    for url in deleted_images:
                        print(url)
                        imgpath = os.path.join(BASE_DIR,url)
                        print(imgpath)
                        if os.path.isfile(imgpath):
                            os.remove(imgpath)

                path = os.path.join(MEDIA_ROOT,space.document_folder)
                fs = FileSystemStorage(location=path)
                document_list = request.FILES.getlist('document_list')
                for doc in document_list:
                    filename = fs.save(doc.name, doc)

                if 'deleted_documents' in request.data:
                    deleted_documents = request.data['deleted_documents']
                    for url in deleted_documents:
                        print(url)
                        docpath = os.path.join(BASE_DIR,url)
                        print(docpath)
                        if os.path.isfile(docpath):
                            os.remove(docpath)

                return success_response(status = status.HTTP_200_OK,message = messages.SPACE_UPDATE_SUCESS,data = '')

def send_space_notification(request):
    notification_list =[]
    available_space = RentalSpace.objects.filter(is_available=True).count()
    available_space_notification = {'message':f"{available_space} Available spaces"}
    notification_list.append(available_space_notification)
    return success_response(status = status.HTTP_200_OK,message = messages.DETAIL_FETCH_SUCCESS,data=notification_list)


def customer_building_dropdown(request):
    user = request.user
    buildings = Contract.objects.filter(customer=user,is_active=True).values('space__building__name','space__building__id')
    serializer = CustomUserBuildingDropdownSerializer(buildings,many=True)
    return success_response(status = status.HTTP_200_OK,message = messages.DETAIL_FETCH_SUCCESS,data=serializer.data)

def customer_space_dropdown(request):
    space__building__id = request.GET.get('space__building__id',None)
    spaces = Contract.objects.filter(customer=user,is_active=True)
    if  space__building__id:
        spaces= spaces.filter(space__building__id=space__building__id)
    spaces = spaces.values('space__code','space__id')
    serializer = CustomUserSpaceDropdownSerializer(spaces,many=True)
    return success_response(status = status.HTTP_200_OK,message = messages.DETAIL_FETCH_SUCCESS,data=serializer.data)
