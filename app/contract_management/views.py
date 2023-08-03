from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from .services import *
from app.contract_management.custom_permissions  import *
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework import generics, permissions

# Create your views here.

class SpaceRequestView(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope,SpaceRequestPermission]

    def post(self, request):
        return create_space_request(request=request)

    def get(self,request):
        return get_space_requests(request=request)

class SpaceRequestDetail(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope,SpaceRequestPermission]

    def put(self, request,id):
        return update_space_request_status(request=request,id=id)

    # def get(self,request,id):
    #     return get_space_requests(request=request)

class ContractView(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope,ContractPermission]

    def post(self, request):
        return create_contract(request=request)

    def get(self,request):
        return get_contract_list(request=request)    
        
class ContractDetailsView(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope,ContractPermission]

    def get(self, request, id):
        return get_contract_details(request=request, id=id)
    
    def put(self, request, id):
        return update_contract_details(request=request, id=id)


# class ContractPdfGeneration(APIView):

#     permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope,ContractPermission]

#     def post(self, request):
#         return create_contract_pdf(request=request)


class UploadContractDocuments(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope,ContractPermission]

    def post(self, request):
        return upload_contract_documents(request=request)
