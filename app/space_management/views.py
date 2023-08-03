from rest_framework.views import APIView
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework import generics, permissions
from .services import *
from app.space_management.custom_permissions  import *

# Create your views here.

class CountryView(APIView):
    def get(self,request):
        res = get_all_country(request)
        return res


class StateView(APIView):
    def get(self,request):
        res=get_all_states(request=request)
        return res


class CityView(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope, CityPermission]

    def get(self,request):
        res=get_all_cities(request=request)
        return res
    
    def post(self,request):
        res=add_new_city(request=request)
        return res
    
class CityUpdateDelete(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope, CityPermission]

    def get(self,request,id):
        res=get_city_details(request=request,id=id)
        return res

    def put(self,request,id):
        res=update_city(request=request,id=id)
        return res
    
    def delete(self,request,id):
        res=delete_city(request=request,id=id)
        return res
    
class Building(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope, BuildingPermission]

    def get(self,request):
        res = get_building(request=request)
        return res
    
    def post(self,request):
        res  = add_new_building(request=request)
        return res
    
class BuildingDeleteUpdate(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope, BuildingPermission]

    def get(self,request,id):
        return get_each_building(request=request,id=id)

    def put(self,request,id):
        return update_building(request=request,id=id)

    def delete(self,request,id):
        return delete_building(request=request,id=id)
    
class RentalSpaceView(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope, RentalSpacePermission]

    def get(self,request):
        return get_spaces(request=request)
    
    def post(self,request):
        return add_new_space(request=request)
    
class RentalSpaceUpdateDelete(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope, RentalSpacePermission]

    def get(self,request,id):
        return get_space_details(request=request,id=id)
    
    def put(self,request,id):
        return update_space(request=request,id=id)
    
    def delete(self,request,id):
        return delete_space(request=request,id=id)
    
class SpaceNotificationView(APIView):
    def get(self,request):
        return send_space_notification(request=request)


class CustomerBuildingDropdown(APIView):
    def get(self,request):
        return customer_building_dropdown(request=request)

class CustomerSpaceDropdown(APIView):
    def get(self,request):
        return customer_space_dropdown(request=request)