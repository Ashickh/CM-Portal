from rest_framework import serializers
from app.contract_management.models import *
from app.invoice_management.models import *
import datetime
from django.db.models import Sum

class CustomerReportSerializer(serializers.ModelSerializer):
    customer_details = serializers.SerializerMethodField(read_only=True)
    space = serializers.SerializerMethodField(read_only=True)
    is_created = serializers.SerializerMethodField(read_only=True)
    def get_customer_details(self,obj):
        try:
            data = {
                "customer_name": obj.customer.first_name,
                "contact_number": obj.customer.phonenumber,
                "email": obj.customer.email,
                "building":obj.space.building.name,
            }
        except:
            data = None
            pass
        return data

    def get_space(self,obj):
        value = obj.space.code
        return value
    def get_is_created(self,obj):
        value = obj.is_created
        datetime_obj = datetime.datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S.%f%z")
        date = datetime_obj.date()
        return date
    class Meta:
        model = Invoice
        fields = ['id','customer_details','space','is_created','invoice_date','total_amount']



class RevenueReportSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField(read_only=True)
    def get_details(self,obj):
        try:
            data = {
                "Country": obj.space.building.city.state.country.name,
                "State": obj.space.building.city.state.name,
                "District": obj.space.building.city.name,
                "building": obj.space.building.name,
                "space": obj.space.code,
                "Revenue": obj.rent_amount
            }
        except:
            data = None
            pass
        return data
    class Meta:
        model = Invoice
        fields = ['id','details']


class BuildingRevenueReportSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField(read_only=True)
    total_revenue = serializers.SerializerMethodField(read_only=True)
    def get_details(self,obj):
        building = Building.objects.get(id=obj['space__building'])
        try:
            data = {
                "Country": building.city.state.country.name,
                "State": building.city.state.name,
                "building": building.name,
                
            }
        except:
            data = None
            pass
        return data
    def get_total_revenue(self, obj):
        return obj['total_revenue']
    
    class Meta:
        model = Invoice
        fields = ['id','details','total_revenue']

    


class AmountDepositedReportSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField(read_only=True)
    def get_details(self,obj):
        try:
            data = {
                "Customer_Name": obj.customer.first_name,
                "Contact_Number": obj.customer.phonenumber,
                "Email_Id": obj.customer.email,
                "space": obj.space.code,
                "Amount_Deposited":obj.security_payment.amount
                
            }
        except:
            data = None
            pass
        return data
    class Meta:
        model = SpaceRequest
        fields = ['id','details']


class SalesReportSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField(read_only=True)
    total_space = serializers.SerializerMethodField(read_only=True)
    total_rent=serializers.SerializerMethodField(read_only=True)
    total_deposit=serializers.SerializerMethodField(read_only=True)
    def get_details(self,obj):
        values = SpaceRequest.objects.filter(space__building_id=obj['space__building'])
        for value in values:
            print("value:",value)
            try:
                data = {
                    "Country": value.space.building.city.state.country.name,
                    "State": value.space.building.city.state.name,
                    "building": value.space.building.name,
                    "City": value.space.building.city.name,
                }
            except:
                data = None
                pass
            return data
           
    def get_total_space(self, obj):
        return obj['total_space']   

    def get_total_rent(self, obj):
        return obj['total_rent']  

    def get_total_deposit(self,obj):
        qs = SpaceRequest.objects.filter(space__building_id=obj['space__building']) 
        qs= (qs.values('space__building').annotate(total_deposit=Sum('security_deposit_payment__amount')))   
        return qs[0]['total_deposit']
    
    class Meta:
        model = Invoice
        fields = ['id','details','total_space','total_rent','total_deposit']

class DocumentReportSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField(read_only=True)
    def get_details(self,obj):
        try:
            documents = obj.documentfolder
            if documents:
                file_names = os.listdir(documents)
               
                flder_path= [os.path.join(documents, filename) for filename in file_names]

            data = {
                "Customer_Name": obj.customer.first_name,
                "Contact_Number": obj.customer.phonenumber,
                "Email_Id": obj.customer.email,
                "building": obj.space.building.name,
                "space": obj.space.code,
                "documents": flder_path
          
            }
            print(data)
        except:
            data = None
            pass
        return data
 
    class Meta:
        model = Contract
        fields = ['id','details']


