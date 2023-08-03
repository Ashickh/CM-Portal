from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
import services
from django.core.mail import send_mail
from rest_framework import status, permissions
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from cm_backend.settings import API_URL

# Create your views here.


# views for features
class FeatureView(APIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    def get(self, request):
        return services.view_features(request=request)
        # return Response(res)
            
    
    def post(self,request):
        return services.feature_creation(request=request)


class FeatureDetailView(APIView):
    def put(self,request,id):
        return services.update_feature(request=request,id=id)
        
    def delete(self,request,id):
        return services.delete_feature(request=request,id=id)


# view for Role    
class RoleView(APIView):
    def get(self, request):
        return services.view_roles(request=request)
            
    
    def post(self,request):
        return services.role_creation(request=request)


class RoleDetailView(APIView):
    def put(self,request,id):
        return services.update_role(request=request,id=id)
        
    def delete(self,request,id):
        return services.delete_role(request=request,id=id)
       
# view for RoleFeature

class RoleFeatureView(APIView):
    def get(self, request):
        return services.view_role_features(request=request)
            
    
    def post(self,request):
        return services.role_feature_creation(request=request)


class RoleFeatureDetailView(APIView):
    def put(self,request,pk):
        return services.update_role_feature(request=request,pk=pk)
        
    def delete(self,request,id):
        return services.delete_role_feature(request=request,id=id)



# view for Admin Users

class UserView(APIView):
    def get(self, request):
        return services.view_users(request=request)
            
    
    def post(self,request):
        return services.user_creation(request=request)

class UserDetailView(APIView):
    def put(self,request,id):
        return services.update_Userdetails(request=request,id=id)
        
    def delete(self,request,id):
        return services.delete_user(request=request,id=id)

# view for UserRole 

class UserRoleView(APIView):
    def get(self, request):
        return services.view_user_roles(request=request)
            
    
    def post(self,request):
        return services.user_role_creation(request=request)


#  view for EmailToken
class EmailTokenView(APIView):
    def get(self, request):
        return services.view_email_tokens(request=request)
            
    
    def post(self,request):
        return services.email_token_creation(request=request)



class PasswordResetEmailView(APIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = CustomUser.objects.get(email=email)
        id=user.id
        email_token =EmailToken.objects.all().values_list('user')
        for em in email_token:
           if id in em :
                user_id = EmailToken.objects.get(id=id)
                token = user_id.token
                subject = 'Password Reset'
                message = f'Click the link below to reset your password:\n\n' \
                        f'{API_URL}/reset-password/{user.id}/{token}/'
                send_mail(subject, message, 'settings.EMAIL_HOST_USER', [email])

                return Response({'detail': 'Password reset link has been sent.'},
                                status=status.HTTP_200_OK)

        return Response({'detail': 'token for this email not created.'},
                            status=status.HTTP_400_BAD_REQUEST)

class UserRoleView(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    def get(self, request):
        return services.view_user_roles(request=request)
            

class reset_passwordView(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    def post(self,request):
        return services.reset_password(request=request)
        

        
       
