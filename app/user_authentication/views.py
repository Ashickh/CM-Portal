from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.user_authentication.serializers import *
from django.contrib.auth import authenticate
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework import generics, permissions
from app.user_authentication import services
from django.core.mail import send_mail

#change password
from constants.responses import responce
from constants import messages 

#pwd reset
from .serializers import *
from cm_backend.settings import API_URL
from django.conf import settings
from cm_backend.settings import EMAIL_HOST_USER

#
from django.contrib.auth.tokens import default_token_generator

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from rest_framework import status, permissions
from app.user_authentication  import custom_permissions
# Create your views here.

class CustomerRegistrationView(APIView):
    def get(self, request):
        return services.view_customer(request=request)
          
    
    def post(self,request):
        return services.customer_registration(request=request)
        

#change_password
class ChangePasswordView(APIView):
  
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    def put(self, request):
        user = request.user
        current_password = request.data.get('current_password')  #pm
        new_password = request.data.get('new_password')
        connfirm_password = request.data.get('confirm_password')

        if not user.check_password(current_password):
            return responce(status=status.HTTP_400_BAD_REQUEST,message=messages.PASSWORD_INCORRECT,data=request.data)

        if new_password== connfirm_password:    

            user.set_password(new_password)
            user.save()
            return responce(status=status.HTTP_200_OK, message=messages.CHANGE_PASSWORD_SUCESS, data=request.data)
        return responce(status=status.HTTP_200_OK, message=messages.PASSWORD_NOT_MATCH, data=request.data)





#add user role
# class UserRoleView(APIView):
#     def post(self,request):
#         role=request.role
#         user=request.user



# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .serializers import UserRegistrationSerializer,UserRole_Serializer

# class UserRegistrationView(APIView):
#     def post(self, request):
#         user = request.data.get('user')
#         userrole = request.data.get('userrole')

#         reg_serializer = UserRegistrationSerializer(data=user)
#         role_serializer = UserRole_Serializer(data=userrole)

#         if reg_serializer.is_valid() and role_serializer.is_valid():
#             reg_instance = reg_serializer.save()
#             role_instance = role_serializer.save()

#             # You can perform any additional operations or validations here

#             return Response({'success': True})
#         else:
#             return Response({'success': False, 'errors': reg_serializer.errors})



# 2) User Login 

class UserLoginView(APIView):
    def post(self, request):
        return services.login(request=request)


# 3.0 token creation     
class EmailTokenView(APIView):
    def get(self, request):
        return services.view_email_tokens(request=request)
            
    
    def post(self,request):
        return services.email_token_creation(request=request)   


# 3) email send with token
class PasswordResetEmailView(APIView):

    def post(self, request, *args, **kwargs):
        return services.send_password_reset_email(request)


class VerifyEmailTokenView(APIView):
    def get(self, request):
        return services.verify_email_token(request=request)




# 3.1 reset pwd
class ResetPasswordView(APIView):
    
    def post(self,request):
        return services.reset_password(request)



# view for Role    
class RoleView(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope, custom_permissions.RolePermission]

    def get(self, request):
        return services.view_roles(request=request)
            
    
    def post(self,request):
        return services.role_creation(request=request)


class RoleListWithoutAdminView(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope, custom_permissions.RolePermission]

    def get(self, request):
        return services.view_roles_without_admin(request=request)



class RoleDetailView(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope, custom_permissions.RolePermission]

    def get(self,request,id):
        return services.get_role_detail(request=request,id=id)

    def put(self,request,id):
        return services.update_role(request=request,id=id)
        
    def delete(self,request,id):
        return services.delete_role(request=request,id=id)


class RoleFeaturesView(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope, custom_permissions.RolePermission]

    # def get(self,request,id):
    #     return services.get_role_detail(request=request,id=id)

    def get(self,request,role_id):
        return services.get_role_features(request=request,role_id=role_id)
        
    def put(self,request,role_id):
        return services.update_role_features(request=request,role_id=role_id)



class UserView(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope, custom_permissions.UserManagementPermission]

    def get(self, request):
        return services.view_users(request=request)
            
    
    def post(self,request):
        return services.user_creation(self,request=request)


class UserDetailView(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope, custom_permissions.UserManagementPermission]

    def get(self,request,id):
        return services.get_each_user(request=request,id=id)

    def put(self,request,id):
        return services.update_user(request=request,id=id)
        
    def delete(self,request,id):
        return services.delete_user(request=request,id=id)


class CustomerDetailView(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope, custom_permissions.CustomerManagementPermission]

    def get(self,request,id):
        return services.get_each_user(request=request,id=id)

    def put(self,request,id):
        return services.update_user(request=request,id=id)
        
    def delete(self,request,id):
        return services.delete_user(request=request,id=id)


class CustomerListView(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope, custom_permissions.CustomerManagementPermission]

    def get(self, request):
        return services.view_customer(request=request)


class SideBarView(APIView):

    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request,role_id):
        return services.get_sidebar(request=request,role_id=role_id)