from rest_framework import serializers
from .models import *
import sys
import traceback
import os
from cm_backend.settings import *
from app.contract_management.models import *

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ['id','name']
    
class StateSerializer(serializers.ModelSerializer):

    class Meta:
        model = State
        fields = ['id','name']
        
class CitySerializer(serializers.ModelSerializer):
   
    class Meta:
        model = City
        fields = ['id','name','is_active','state']
    
class BuildingSerializer(serializers.ModelSerializer):


    state_id = serializers.SerializerMethodField(read_only=True)
    
    def get_state_id(self,obj):
        return obj.city.state.id


    class Meta:
        model=Building
        # fields = '__all__'
        exclude = ('image_folder', )
        read_only_fields = ['state_id']

        # fields = ['name','address','phonenumber','electricity_charge','water_charge','maintenance_charge','city_id','image_folder']

    def create(self, validated_data):
        building = self.Meta.model(**validated_data)
        building.image_folder='building'
        building.full_clean()
        building.save() 
        building_path = "building_"+str(building.id)+'/'   
        building.image_folder=building_path
        building.is_active = True
        building.save()
        path = os.path.join(MEDIA_ROOT,building_path)
        os.mkdir(path)
        return building

class RentalSpaceSerializer(serializers.ModelSerializer):
    building_name = serializers.ReadOnlyField(source='building.name')
    is_requested = serializers.SerializerMethodField(read_only=True)
    
    def get_is_requested(self,obj):
        user =self.context['request'].user
        space_request = SpaceRequest.objects.filter(space=obj,customer=user,is_active=True)
        if space_request.exists():
            return True
        else:
            return False

    class Meta:
        model=RentalSpace
        exclude  = ('image_folder','document_folder')
        read_only_fields = ['is_requested']

    def create(self, validated_data):
        space = self.Meta.model(**validated_data)
        space.image_folder='imagefolder'
        space.document_folder='documentfolder'
        space.full_clean()
        space.save() 
        space_folder_url = space.building.image_folder+"space_"+str(space.id)+'/'
        space_url = os.path.join(MEDIA_ROOT,space_folder_url)
        os.mkdir(space_url)

        image_folder_path= space.building.image_folder +"space_"+str(space.id)+'/images/' 
        document_folder_path = space.building.image_folder +"space_"+str(space.id)+'/documents/'
        bill_folder_path = space.building.image_folder +"space_"+str(space.id)+'/bills/'
        grivance_folder_path = space.building.image_folder +"space_"+str(space.id)+'/grievances/'

        electricity_folder_path = space.building.image_folder +"space_"+str(space.id)+'/bills/electicity/'
        water_folder_path = space.building.image_folder +"space_"+str(space.id)+'/bills/water/'

        space.image_folder=image_folder_path
        space.document_folder=document_folder_path
        space.is_active = True
        space.is_available = True
        space.save()

        image_folder =os.path.join(MEDIA_ROOT,image_folder_path)
        os.mkdir(image_folder)
        document_folder =os.path.join(MEDIA_ROOT,document_folder_path)
        os.mkdir(document_folder)
        bill_folder =os.path.join(MEDIA_ROOT,bill_folder_path)
        os.mkdir(bill_folder)
        grivance_folder =os.path.join(MEDIA_ROOT,grivance_folder_path)
        os.mkdir(grivance_folder)

        electicity_folder =os.path.join(MEDIA_ROOT,electricity_folder_path)
        os.mkdir(electicity_folder)
        water_folder =os.path.join(MEDIA_ROOT,water_folder_path)
        os.mkdir(water_folder)
        return space


















    #     path = os.path.join(MEDIA_ROOT,building_path)
    #     fs = FileSystemStorage(location=path)
    #     image_list = self.request.FILES.getlist('image_list')
    #     for img in image_list:
    #         filename = fs.save(img.name, img)


    # def update(self, instance, validated_data):
    #     for attr, value in validated_data.items():
    #         if attr == 'password':
    #             instance.set_password(value)
    #         else:
    #             setattr(instance, attr, value)
    #     instance.save()
    #     return instance


# class BuildingUpdateSerializer(serializers.ModelSerializer):
#     imgurls = serializers.ListField()
#     class Meta:
#         model=Building
#         fields = ['name','address','phonenumber','electricity_charge','water_charge','maintenance_charge','city','imgurls']

# class RentalSpaceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=RentalSpace
#         exclude  = ('image_folder','document_folder')



# class RentalSpaceUpdateSerializer(serializers.ModelSerializer):
#     doclist = serializers.ListField()
#     imglist  =serializers.ListField()
#     class Meta:
#         model = RentalSpace
#         fields = ['code','area','floor','rent_price','description','building_id','min_period','city','doclist','imglist']
#         read_only_fields = ['imglist','doclist']


class AvailableSpaceSerializer(serializers.ModelSerializer):
    building = serializers.SerializerMethodField(read_only=True)
    
    def get_building(self,obj):
        return obj.building.name
        
    class Meta:
        model = RentalSpace
        fields = ['id','code','building']


class CustomUserBuildingDropdownSerializer(serializers.Serializer):
    space__building__name = serializers.CharField()
    space__building__id = serializers.IntegerField()


class CustomUserSpaceDropdownSerializer(serializers.Serializer):
    space__code = serializers.CharField()
    space__id = serializers.IntegerField()