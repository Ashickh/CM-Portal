from rest_framework import serializers
from app.invoice_management.models import *
from app.user_authentication.models import *
from cm_backend.settings import *
from app.space_management.models import *
import os
from django.core.files.storage import FileSystemStorage
from django.db import transaction
import pathlib
# class InvoiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=UtilityReading
#         # fields='__all__'
#         exclude  = ('electricityreading_image','waterreading_image',)

#     def create(self, validated_data):
#         utility=self.Meta.model(**validated_data)
#         utility.save()

#         ebill_folder_path = utility.electricityreading_image +"space_"+str(utility.id)+'/bills/'
#         wbill_folder_path = utility.waterreading_image +"space_"+str(utility.id)+'/bills/'

#         utility.is_active = True

#         ebill_folder =os.path.join(MEDIA_ROOT,ebill_folder_path)
#         wbill_folder =os.path.join(MEDIA_ROOT,wbill_folder_path)
  
#         utility.save()

#         return utility

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=UtilityReading
        exclude  = ('electricityreading_image','waterreading_image',)

    def create(self, validated_data):
       utility=self.Meta.model(**validated_data)
       # utility.save()
       utility.is_active = True
       utility.save()
       return utility


class UtilityReading_ApprovedSerializers(serializers.Serializer):
   
    class Meta:
        model = UtilityReading
        fields = ['approved_by'] 

    
class UtilityList_Serializer(serializers.ModelSerializer):
    electricityreading_image = serializers.SerializerMethodField()
    waterreading_image = serializers.SerializerMethodField()
    building_id = serializers.SerializerMethodField()
    space_code = serializers.SerializerMethodField()

    def get_electricityreading_image(self,obj):
        return  MEDIA_URL + obj.electricityreading_image

    def get_waterreading_image(self,obj):
        return  MEDIA_URL + obj.waterreading_image

    def get_building_id(self,obj):
        return  obj.space.building.id

    def get_space_code(self,obj):
        return  obj.space.code

    class Meta:
        model=UtilityReading
        fields = ['id','month','year','electricity_reading','electricityreading_image','water_reading','waterreading_image',
            'is_active','space','is_created','is_updated','is_active','is_approved','approved_by','building_id','space_code']


class GrievancesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grievances
        exclude = ['issue_image_folder']

    def create(self, validated_data):
        with transaction.atomic():
            issue_image_folder = self.context['request'].FILES.getlist('issue_image_folder')
            grievances = Grievances.objects.create(**validated_data)
            bid = grievances.space.building.id
            sid = grievances.space.id
            gid= grievances.id
            issue_image_folder_path = f"building_{bid}/space_{sid}/grievances/grievance_{gid}/"
            grievances.issue_image_folder = issue_image_folder_path
            grievances.is_active=True
            grievances.save()
            folder_path = os.path.join(MEDIA_ROOT, issue_image_folder_path)
            os.mkdir(folder_path)
            fs = FileSystemStorage(location=folder_path)
            for img in issue_image_folder:
                filename = fs.save(img.name, img)
                    # issue_image_folder_path = "building_"+str(bid)+"/space_"+str(sid)+"/grievances/"+str(gid)+"/"+filename
                    # grievances.issue_image_folder=issue_image_folder_path
                    # grievances.save()
            return grievances


class GrievancesAssigningSerializer(serializers.ModelSerializer):
    class Meta:
        model=Grievances
        fields  = ['assignee','issue_status']


class ChangeGrievancesStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=Grievances
        fields  = ['issue_status']


class GrievancesListSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    space = serializers.SerializerMethodField()

    def get_customer(self,obj):
        return obj.customer.get_full_name()

    def get_space(self,obj):
        print(obj.space.code)
        return obj.space.code

    class Meta:
        model=Grievances
        fields = '__all__'     


class GrievanceDetailSerializer(serializers.ModelSerializer):
    issue_image_folder = serializers.SerializerMethodField()
    is_created = serializers.SerializerMethodField()
    is_updated = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    space = serializers.SerializerMethodField()
    assignee = serializers.SerializerMethodField()

    def get_customer(self,obj):
        return obj.customer.get_full_name()

    def get_assignee(self,obj):
        if obj.assignee:
            return obj.assignee.get_full_name()
        else:
            return None

    def get_space(self,obj):
        return obj.space.code

    def get_is_created(self,obj):
        return obj.is_created.strftime(DATE_TIME_FORMAT)

    def get_is_updated(self,obj):
        return obj.is_updated.strftime(DATE_TIME_FORMAT)

    def get_issue_image_folder(self,obj):
        path = os.path.join(MEDIA_ROOT,obj.issue_image_folder)
        arr = os.listdir(path)
        arr = [f.name for f in pathlib.Path(path).iterdir() if f.is_file()]
        print(arr)
        for index,item in enumerate(arr):
            arr[index] = MEDIA_URL+obj.issue_image_folder+item
        document_urls = arr
        print(document_urls)
        return document_urls

    class Meta:
        model = Grievances
        fields = '__all__' 


class CustomerDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id','first_name','last_name','address','email','phonenumber']


class CustomerSpaceDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RentalSpace
        fields = ['id','code','building__id','building__name','email','phonenumber']


class BillListSerializer(serializers.ModelSerializer):
    customer = CustomerDetailsSerializer()
    space = CustomerSpaceDetailsSerializer()

    class Meta:
        model = Invoice
        fields = "__all__"
    
class InvoiceListSerializer(serializers.ModelSerializer):
    customer = CustomerDetailsSerializer()
    space = CustomerSpaceDetailsSerializer()

    def get_rent_amount(self,obj):
        queryset = self.context['queryset'].filter(space=obj.space,customer=obj.customer)
        return queryset.aggregate(Sum('rent_amount'))['rent_amount__sum']

    def get_water_charge(self,obj):
        queryset = self.context['queryset'].filter(space=obj.space,customer=obj.customer)
        return queryset.aggregate(Sum('water_charge'))['water_charge__sum']


    def get_electricity_charge(self,obj):
        queryset = self.context['queryset'].filter(space=obj.space,customer=obj.customer)
        return queryset.aggregate(Sum('electricity_charge'))['electricity_charge__sum']


    def get_maintenance_charge(self,obj):
        queryset = self.context['queryset'].filter(space=obj.space,customer=obj.customer)
        return queryset.aggregate(Sum('maintenance_charge'))['maintenance_charge__sum']


    def get_total_amount(self,obj):
        queryset = self.context['queryset'].filter(space=obj.space,customer=obj.customer)
        return queryset.aggregate(Sum('total_amount'))['total_amount__sum']


    def get_late_fee(self,obj):
        queryset = self.context['queryset'].filter(space=obj.space,customer=obj.customer)
        return queryset.aggregate(Sum('late_fee'))['late_fee__sum']


    class Meta:
        model = Invoice
        fields = "__all__"

class Notification_ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification_Content
        fields = "__all__"