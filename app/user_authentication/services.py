import json
import requests

from rest_framework import status
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.template.loader import render_to_string

from common.services import *
from constants import messages
from constants.responses import *
from cm_backend.settings import *
from app.user_authentication.serializers import *
from app.user_authentication.models import *


def view_customer(request):
    customer_ids = list(UserRole.objects.filter(role__id=2,is_active=True).values_list('user_id',flat=True))
    customers = CustomUser.objects.filter(id__in=customer_ids,is_active=True)
    serializer = CustomerRegistrationSerializer(customers, many=True)
    return success_response(status=status.HTTP_200_OK,message=messages.CUSTOMER_LIST_SUCESS,data=serializer.data)
 
def customer_registration(request):
    serializer = CustomerRegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return success_response(status=status.HTTP_200_OK,message=messages.CUSTOMER_CREATION_SUCESS,data=serializer.data)

def oauth_login(username, password):
    url = API_URL + 'o/token/'
    print(url)
    client_id = 'Ws48HXt7OVMPE9EgpV7ieZ7fvtnu9cErYt38te8R'
    client_secret = 'OwgB9SaZSA9NsRpbHChqFGNh4TtQr3ofy2R1b9Zm51RFoKwvfoqIEyPn0G2rHo63JWC0OGRziaOrQo1fLPTvrnDxEI19H9hvlWLlyPIPkQUTpl3dBTFUMAtv1Edo1x33'
    data = [
        ('grant_type', 'password'),
        ('username', username),
        ('password', password),
    ]
    response = requests.post(url, data=data, auth=(client_id, client_secret), verify=False)
    print("=======>>>",response)
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    print(data)
    response = requests.post(url, data=data)
    data = response.json()
    data["status"]=response.status_code
    return data

def login(request):
    serializer = LoginSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        uname = serializer.validated_data["username"]
        username=uname.lower()
        password = serializer.validated_data["password"]

        try:
            user = CustomUser.objects.get(Q(email__iexact = username) | Q(phonenumber__iexact = username))
        except CustomUser.DoesNotExist:
            return failure_response(status = status.HTTP_400_BAD_REQUEST,message = messages.USER_NOT_REGISTERED,data = '')

        username = user.email
        results= oauth_login(username, password)

        if results["status"] == 200:
            results["id"] = user.id
            results["role"] = UserRole.objects.get(user = user).role.name
            return success_response(status = status.HTTP_200_OK,message = messages.LOGIN_SUCCESS,data = results)
        else:
            return failure_response(status = status.HTTP_401_UNAUTHORIZED,message = messages.LOGIN_FAIL,data = results)



def send_password_reset_email(request):
    serializer = PasswordResetEmailSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.validated_data['email']

        try:
            user = CustomUser.objects.get(email__iexact=email,is_active=True)
        except ObjectDoesNotExist:
            return failure_response(status=status.HTTP_400_BAD_REQUEST,message=messages.USER_NOT_REGISTERED,data='')   

        token = str(uuid.uuid4())
        EmailToken.objects.filter(user=user,is_active=True).update(is_active=False)
        EmailToken.objects.create(token=token,user=user)

        url = FRONT_END_URL+'password_reset/'+token
        html_content = render_to_string(str(BASE_DIR)+'/templates/email_templates/password_reset_email.html', {'url':url})
        subject = 'Password Reset Email'
        # result = send_mail(EMAIL_HOST_USER,email,subject,html_content)
        result = send_mail(email,subject,html_content)

        if result == True:
            return success_response(status=status.HTTP_200_OK,message=messages.PASSWORD_CHANGE_MAIL_SUCESS,data='')
        else:
            return failure_response(status=status.HTTP_400_BAD_REQUEST,message='Error in mail send',data='')


def verify_email_token(request):
    token = request.GET.get('token', None)
    try:
        email_token = EmailToken.objects.get(token=token,is_active=True)
    except EmailToken.DoesNotExist:
        return failure_response(status=status.HTTP_400_BAD_REQUEST,message='Invalid token',data='')
    return success_response(status=status.HTTP_200_OK,message='Valid token',data='')


def reset_password(request):
    serializer = ChangePasswordSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            email_token = EmailToken.objects.get(token=token,is_active=True)
        except EmailToken.DoesNotExist:
            return failure_response(status=status.HTTP_400_BAD_REQUEST,message='Invalid token',data='')

        if  email_token.user.check_password(new_password) == True:
            return failure_response(status=status.HTTP_400_BAD_REQUEST,message=messages.CHANGE_PASSWORD_OLD_PASSWORD,data='')


        with transaction.atomic():
            user = email_token.user
            user.set_password(new_password)
            user.is_verified =True
            email_token.is_active = False
            email_token.save()
            user.save()
            return success_response(status=status.HTTP_200_OK,message=messages.PASSWORD_CHANGE_SUCESS,data='')

def role_creation(request):
    serializer = RoleSerializer(data=request.data)
    if serializer.is_valid(raise_exception = True):
        if Role.objects.filter(name__iexact=serializer.validated_data['name'],is_active=True):
            return failure_response(status=status.HTTP_400_BAD_REQUEST,message=messages.DUPLICATE_ROLE_EXIST,data='')
        else:
            with transaction.atomic():
                role = serializer.save()

                role.is_active = True
                role.save()

                feature_list = Feature.objects.all()
                for feature in  feature_list:
                    RoleFeature.objects.create(role=role,feature=feature)
                return success_response(status=status.HTTP_201_CREATED,message=messages.ROLE_CREATION_SUCESS,data=serializer.data)



def view_roles(request):   
    all_roles = Role.objects.filter(is_active=True)
    serializer = RoleSerializer(all_roles, many=True)
    return success_response(status=status.HTTP_201_CREATED,message=messages.ROLE_DETAILS_FETCH_SUCCESS,data=serializer.data)

def view_roles_without_admin(request):   
    all_roles = Role.objects.filter(is_active=True).exclude(id=1)
    serializer = RoleSerializer(all_roles, many=True)
    return success_response(status=status.HTTP_201_CREATED,message=messages.ROLE_DETAILS_FETCH_SUCCESS,data=serializer.data)        
                 
def get_role_detail(request,id):
    role_obj = Role.objects.get(id=id)
    serializer = RoleSerializer(role_obj)
    return success_response(status=status.HTTP_200_OK,message=messages.ROLE_DETAILS_FETCH_SUCCESS,data=serializer.data)


def update_role(request,id):
    role_obj = Role.objects.get(id=id,is_active=True)
    serializer = RoleSerializer(data=request.data, instance=role_obj,partial=True)
    if serializer.is_valid(raise_exception = True):
        name = serializer.validated_data['name']
        if Role.objects.filter(name=name,is_active=True).exclude(id=id).exists():
            return failure_response(status=status.HTTP_400_BAD_REQUEST,message=messages.DUPLICATE_ROLE_EXIST,data='')
        else:
            with transaction.atomic():

                # role = RoleSerializer(data=serializer.validated_data, instance=role_obj)
                serializer.save()
                return success_response(status = status.HTTP_200_OK,message = messages.ROLE_UPDATE_SUCESS,data = '')




def delete_role(request,id):
    role = Role.objects.get(id=id,is_active=True)
    with transaction.atomic():
        role.is_active = False
        role.save()
        RoleFeature.objects.filter(role=role,is_active=True).update(is_active=False)
        return success_response(status = status.HTTP_200_OK,message = messages.ROLE_DELETE_SUCESS,data = '')




def get_role_features(request,role_id):
    role = Role.objects.get(id=role_id,is_active=True)
    role_features = RoleFeature.objects.filter(role = role ,is_active=True)
    result =  RoleFeatureSerializer(role_features, many=True).data
    return success_response(status = status.HTTP_200_OK,message = messages.ROLE_FEATURE_FETCH_SUCESS,data = result)




def update_role_features(request,role_id):
    try:
        features = request.data['features']
        with transaction.atomic():
            for item in features:
                detail = RoleFeature.objects.get(pk=item['id'])
                serializer = RoleFeatureSerializer(detail, data=item,partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            return success_response(status = status.HTTP_200_OK,message = messages.ROLE_FEATURE_UPDATE_SUCESS,data = '')
    except ValidationError as e:
        return validation_error_response(e)
    except Exception as e:
        return error_response() 

                   

def user_creation(self,request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception = True):
        # if CustomUser.objects.filter(Q(email=serializer.validated_data['email'])|Q(phonenumber=serializer.validated_data['phonenumber'])).exists():
        #     return failure_response(status=status.HTTP_400,message=messages.ROLE_DUPLICATE,data='')
        # else:
        with transaction.atomic():
            user = serializer.save()
            token = str(uuid.uuid4())
            EmailToken.objects.create(token=token,user=user)

            url = FRONT_END_URL+'password_reset/'+token
            html_content = render_to_string(str(BASE_DIR)+'/templates/email_templates/password_reset_email.html', {'url':url})
            subject = 'Password Reset Email'
            # result = send_mail(EMAIL_HOST_USER,user.email,subject,html_content)
            result = send_mail(user.email,subject,html_content)
            if result == True:
                return success_response(status=status.HTTP_200_OK,message=messages.USER_CREATION_SUCESS,data='')

def view_users(request):
    role = request.GET.get('role',None)
    user_roles = UserRole.objects.filter(is_active=True).exclude(role__id__in=[1,2])
    if role:
        user_roles = user_roles.filter(role__id=role)
    user_ids = list(user_roles.values_list('user_id',flat=True))
    users = CustomUser.objects.filter(id__in=user_ids,is_active=True)
    serializer = UserSerializer(users, many=True)
    return success_response(status=status.HTTP_201_CREATED,message=messages.USER_DETAILS_FETCH_SUCCESS,data=serializer.data)


def get_each_user(request,id):
    user = CustomUser.objects.get(id=id)
    serializer = UserDetailSerializer(user)
    return success_response(status=status.HTTP_200_OK,message=messages.USER_DETAILS_FETCH_SUCCESS,data=serializer.data)



def update_user(request,id):
    with transaction.atomic():
        user = CustomUser.objects.get(id=id)
        serializer = UserSerializer(data=request.data, instance=user)
        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data)
            user =serializer.save()
            return success_response(status=status.HTTP_200_OK,message=messages.USER_UPDATE_SUCESS,data='')


def  delete_user(request,id):
    user = CustomUser.objects.get(id=id,is_active=True)
    serializer = UserDeleteSerializer(user,{"is_active":False},partial = True)
    if serializer.is_valid():
        user=serializer.save()
        userrole =UserRole.objects.get(user=user)
        userrole.is_active = False
        userrole.save()
        return success_response(status=status.HTTP_200_OK,message=messages.USER_DELETE_SUCESS,data='')


def get_sidebar(request,role_id):
    role = Role.objects.get(id=role_id,is_active=True)
    role_features = RoleFeature.objects.filter(role = role ,is_active=True,feature__is_active=True)
    role_features = role_features.filter(Q(view=True)|Q(edit=True)|Q(delete=True)|Q(create=True))
    result =  RoleFeatureSerializer(role_features, many=True).data
    return success_response(status = status.HTTP_200_OK,message = messages.ROLE_FEATURE_FETCH_SUCESS,data = result)