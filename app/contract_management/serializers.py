from dataclasses import fields
from rest_framework import serializers
import uuid
from app.contract_management.models import *
import os
from django.core.files.storage import FileSystemStorage
from django.db import transaction
import pathlib
from cm_backend.settings import *

class SpaceRequestSerializer(serializers.ModelSerializer):
    space_code = serializers.SerializerMethodField(read_only=True)
    customer_name = serializers.SerializerMethodField(read_only=True)

    def get_space_code(self,obj):
        value = obj.space.code
        return value

    def get_customer_name(self,obj):
        value = obj.customer.get_full_name()
        return value

    class Meta:
        model = SpaceRequest
        fields = "__all__"
        read_only_fields = ['space_code','customer_name']

class SpaceRequestStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceRequest
        fields = ["status"]

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        exclude  = ('documentfolder',)

class ContractDetailsSerializer(serializers.ModelSerializer):
    customer_address = serializers.SerializerMethodField(read_only=True)

    def get_customer_address(self,obj):
        value = obj.contract.customer.address
        return value
        
    class Meta:
        model = ContractDetails
        fields = "__all__"
        read_only_fields = ['customer_address']



class ContractGetSerializer(serializers.ModelSerializer):
    space = serializers.SerializerMethodField(read_only=True)
    customer_name = serializers.SerializerMethodField(read_only=True)
    documentfolder = serializers.SerializerMethodField(read_only=True)

    def get_space(self,obj):
        value = obj.space.code
        return value

    def get_customer_name(self,obj):
        value = obj.customer.get_full_name()
        return value

    def get_documentfolder(self,obj):
        path = os.path.join(MEDIA_ROOT,obj.documentfolder)
        arr = os.listdir(path)
        arr = [f.name for f in pathlib.Path(path).iterdir() if f.is_file()]
        print(arr)
        for index,item in enumerate(arr):
            arr[index] = MEDIA_URL+obj.documentfolder+item
        document_urls = arr
        print(document_urls)
        return document_urls

    class Meta:
        model = Contract
        fields = ['id','space','status','valid_from','valid_to','customer_name','documentfolder']


class ContractDocumentSerializer(serializers.Serializer):
    file = serializers.ListField(child=serializers.FileField())
    contract_id=serializers.IntegerField()
    
    def validate_file(self, value):
        for file in value:
            if file.size == 0:
                raise serializers.ValidationError("File is empty.")
        return value
