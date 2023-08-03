from asyncio import constants
from functools import partial
from venv import create
from xml.sax.handler import all_features
from .models import *
from .serializers import *
from rest_framework import status
from constants import messages
from constants import responses
from rest_framework.response import Response
from django.db import transaction
import json

# from django.contrib.auth.models import User

def view_features(request):   
    # response = {"status":status.HTTP_400_BAD_REQUEST,"message":messages.FEATURE_DETAILS_FAILED}
    all_features = Feature.objects.filter(is_active=True)
    serializer = FeatureSerializer(all_features, many=True)
    return response(status=status.HTTP_200_OK,message=messages.FEATURE_DETAILS_SUCESS,data=serializer.data)



def feature_creation(request):
    # response = {"status":status.HTTP_400_BAD_REQUEST,"message":messages.FEATURE_CREATION_FAILED}
    serializer = FeatureSerializer(data=request.data)
    name = request.data['name']
    with transaction.atomic():
        try:
            if Feature.objects.filter(name=name).exists():
                feture = Feature.objects.get(name=name)
                return response(status=status.HTTP_400_BAD_REQUEST,message=messages.FEATURE_ADD_DUPLICATE,data=[])
    
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return response(status=status.HTTP_201_CREATED,message=messages.FEATURE_CREATION_SUCESS,data=serializer.data)
            return response (status=status.HTTP_400_BAD_REQUEST,message=messages.FEATURE_CREATION_FAILED)
        except Exception as e:
            return response(status=status.HTTP_400_BAD_REQUEST,message=messages.FEATURE_CREATION_FAILED,data=[])
                

def update_feature(request,id):
    try:
        feature = Feature.objects.get(id=id)
        if feature.is_active == False:
            return response(status=status.HTTP_400_BAD_REQUEST,message=messages.FEATURE_UPDATE_FAIL,data=[])
        if feature:
            serializer = FeatureSerializer(data=request.data, instance=feature)
            if serializer.is_valid():
                name = serializer.validated_data.get("name")
                feature.name = name
                feature.save()
                return response(status=status.HTTP_200_OK, message=messages.FEATURE_UPDATE_SUCESS, data=serializer.data)
            return response(status=status.HTTP_400_BAD_REQUEST, message=messages.FEATURE_UPDATE_FAIL, data=[])
    except Exception as e:
        return response(status=status.HTTP_400_BAD_REQUEST, message=messages.FEATURE_UPDATE_FAIL, data=[])


def  delete_feature(request,id):
    try:
        feature = Feature.objects.get(id=id)
        if feature.is_active == False:
           return response(status=status.HTTP_400_BAD_REQUEST,message=messages.FEATURE_DELETE_FAIL,data=[])
        if feature:
            serializer = FeatureSerializer(feature,{"is_active":False},partial = True)
            if serializer.is_valid():
                serializer.save()
                return response(status=status.HTTP_200_OK, message=messages.FEATURE_DELETE_SUCESS, data=[])
        return response(status=status.HTTP_400_BAD_REQUEST,message=messages.FEATURE_DELETE_FAIL,data=serializer.data)
    except Exception as e:
       return response(status=status.HTTP_400_BAD_REQUEST,message=messages.FEATURE_DELETE_FAIL,data=serializer.data)

            


# role Services

def view_roles(request):   
    all_roles = Role.objects.all()
    serializer = RoleSerializer(all_roles, many=True)
    return response(status=status.HTTP_200_OK,message=messages.ROLE_DETAILS_SUCESS, data=serializer.data)
    

def role_creation(request):
    serializer = RoleSerializer(data=request.data)
    name = request.data['name']
    with transaction.atomic():
        try:
            if Role.objects.filter(name=name).exists():
                role = Role.objects.get(name=name)
                return response(status=status.HTTP_400_BAD_REQUEST,message=messages.ROLE_ADD_DUPLICATE,data=[])
            if serializer.is_valid(raise_exception=True):
                role = serializer.save()
                features = Feature.objects.all()
                print(features)
                for feature in  features:
                    RoleFeature.objects.create(role=role,feature=feature)
                return response(status=status.HTTP_201_CREATED, message=messages.ROLE_CREATION_SUCESS, data=serializer.data)
            return response(status=status.HTTP_400_BAD_REQUEST,message=messages.ROLE_CREATION_FAILED,data=[])
        except Exception as e:
            return response(status=status.HTTP_400_BAD_REQUEST,message=messages.ROLE_CREATION_FAILED,data=[])


def update_role(request,id):
    with transaction.atomic():
        try:
            role = Role.objects.get(id=id)
            if role.is_active == False:
                return response(status=status.HTTP_400_BAD_REQUEST,message=messages.ROLE_UPDATE_FAIL,data=[])
            if role:
                serializer = RoleSerializer(data=request.data, instance=role)
                if serializer.is_valid():
                    name = serializer.validated_data.get("name")
                    role.name = name
                    role.save()
                    return response(status=status.HTTP_200_OK, message=messages.ROLE_UPDATE_SUCESS, data=serializer.data)
                return response(status=status.HTTP_400_BAD_REQUEST, message=messages.ROLE_UPDATE_FAIL, data=[])
        except Exception as e:
            return response(status=status.HTTP_400_BAD_REQUEST, message=messages.ROLE_UPDATE_FAIL, data=[])

def  delete_role(request,id):
    try:
        role = Role.objects.get(id=id)
        if role.is_active == False:
           return response(status=status.HTTP_400_BAD_REQUEST, message=messages.ROLE_DELETE_FAIL, data=[])
        if role:
            serializer = RoleSerializer(role,{"is_active":False},partial = True)
            if serializer.is_valid():
                serializer.save()
                return response(status=status.HTTP_200_OK, message=messages.ROLE_DELETE_SUCESS, data=[])
        return response(status=status.HTTP_400_BAD_REQUEST, message=messages.ROLE_DELETE_FAIL, data=serializer.data)
    except Exception as e:
       return response(status=status.HTTP_400_BAD_REQUEST, message=messages.ROLE_DELETE_FAIL, data=serializer.data)


# RoleFeature Services

def view_role_features(request):   
    query_set = RoleFeature.objects.all()
    serializer = RoleFeatureSerializer(query_set, many=True)
    return response(status=status.HTTP_200_OK,message=messages.ROLE_FEATURE_DETAILS_SUCESS, data=serializer.data)


def update_role_feature(request,pk):
        items = request.data
        for item in items:
            print(item)
            try:
                detail = RoleFeature.objects.get(pk=item['id'])
                if detail.is_active == False:
                  return response(status=status.HTTP_400_BAD_REQUEST,message=messages.ROLE_FEATURE_UPDATE_FAIL,data=[])
                serializer = RoleFeatureSerializer(detail, data=item)
                if serializer.is_valid():
                    created = RoleFeature.objects.filter(pk=item['id']).update(**item)
            except Exception as e:
                return response(status=status.HTTP_400_BAD_REQUEST, message=messages.ROLE_FEATURE_UPDATE_FAIL, data=[])
        return response(status=status.HTTP_200_OK, message=messages.ROLE_FEATURE_UPDATE_SUCESS, data=serializer.data)

    
   

def  delete_role_feature(request,id):
    try:
        query_set = RoleFeature.objects.get(id=id)
        if query_set.is_active == False:
           return response(status=status.HTTP_400_BAD_REQUEST, message=messages.ROLE_FEATURE_DELETE_FAIL, data=[])
        if query_set:
            serializer = RoleSerializer(query_set,{"is_active":False},partial = True)
            if serializer.is_valid():
                serializer.save()
                return response(status=status.HTTP_200_OK, message=messages.ROLE_FEATURE_DELETE_SUCESS, data=[])
        return response(status=status.HTTP_400_BAD_REQUEST, message=messages.ROLE_FEATURE_DELETE_FAIL, data=serializer.data)
    except Exception as e:
       return response(status=status.HTTP_400_BAD_REQUEST, message=messages.ROLE_FEATURE_DELETE_FAIL, data=serializer.data)



# AdminUsers Services

def view_users(request):   
    query_set = CustomUser.objects.all()
    serializer = UserSerializer1(query_set, many=True)
    return response(status=status.HTTP_200_OK,message=messages.USER_DETAILS_SUCESS, data=serializer.data)

def user_creation(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user =serializer.save()
        role_id = request.data.get('role')
        role = Role.objects.get(pk=role_id)
        user_role_serializer = UserRoleSerializer(data={'user': user.id, 'role': role.id})
        if user_role_serializer.is_valid():
            user_role_serializer.save()
            return Response(data=user_role_serializer.data, status=status.HTTP_201_CREATED)
        return response(status=status.HTTP_201_CREATED, message=messages.USER_CREATION_SUCESS, data=serializer.data)
    return response(status=status.HTTP_400_BAD_REQUEST, message=messages.USER_CREATION_FAILED, data=[])

def update_Userdetails(request,id):
    with transaction.atomic():
        try:
            query_set = CustomUser.objects.get(id=id)
            print(query_set)
            if query_set.is_active == False:
                return response(status=status.HTTP_400_BAD_REQUEST,message=messages.USER_UPDATE_FAIL,data=[])
            if query_set:
                serializer = UserSerializer(data=request.data, instance=query_set,partial=True)
                print(serializer)
                if serializer.is_valid(raise_exception=True):
                    
                    user =serializer.save()
                    role_id = request.data.get('role')
                    role = Role.objects.get(id=role_id)
                    user_role = UserRole.objects.get(user=user) 
                    user_role_serializer = UserRoleSerializer(instance=user_role, data={'user': user.id, 'role': role.id})
                    if user_role_serializer.is_valid():
                        user_role_serializer.save()
                    return response(status=status.HTTP_200_OK, message=messages.USER_UPDATE_SUCESS, data=serializer.data)
                else:
                    return response(status=status.HTTP_400_BAD_REQUEST, message=messages.USER_UPDATE_FAIL, data=[])
        except Exception as e:
            print(e)
            return response(status=status.HTTP_400_BAD_REQUEST, message=messages.USER_UPDATE_FAIL, data=[])

def  delete_user(request,id):
    try:
        query_set = CustomUser.objects.get(id=id)
        if query_set.is_active == False:
           return response(status=status.HTTP_400_BAD_REQUEST, message=messages.USER_DELETE_FAIL, data=[])
        if query_set:
            serializer = UserSerializer(query_set,{"is_active":False},partial = True)
            if serializer.is_valid():
                serializer.save()
                return response(status=status.HTTP_200_OK, message=messages.USER_DELETE_SUCESS, data=[])
        return response(status=status.HTTP_400_BAD_REQUEST, message=messages.USER_DELETE_FAIL, data=serializer.data)
    except Exception as e:
       return response(status=status.HTTP_400_BAD_REQUEST, message=messages.USER_DELETE_FAIL, data=serializer.data)

# UserRole services

def view_user_roles(request):   
    query_set = UserRole.objects.all()
    serializer = UserRoleSerializer(query_set, many=True)
    return response(status=status.HTTP_200_OK,message=messages.USER_ROLE_DETAILS_SUCESS, data=serializer.data)

# def user_role_creation(request):
#     serializer = UserRoleSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save()
#         return response(status=status.HTTP_201_CREATED, message=messages.USER_ROLE_CREATION_SUCESS, data=serializer.data)
#     return response(status=status.HTTP_400_BAD_REQUEST, message=messages.USER_ROLE_CREATION_FAILED, data=[])


# EmailToken services

def view_email_tokens(request):   
    query_set = EmailToken.objects.all()
    serializer = EmailTokenSerializer(query_set, many=True)
    return response(status=status.HTTP_200_OK,message=messages.EMAIL_TOKEN_DETAILS_SUCESS, data=serializer.data)

def email_token_creation(request):
    serializer = EmailTokenSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return response(status=status.HTTP_201_CREATED, message=messages.EMAIL_TOKEN_CREATION_SUCESS, data=serializer.data)
    return response(status=status.HTTP_400_BAD_REQUEST, message=messages.EMAIL_TOKEN_DETAILS_FAILED, data=[])

def reset_password(request):
    try:
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        email_token = EmailToken.objects.get(token=token)
        user_id = email_token.user.id
        emailtoken = EmailToken.objects.filter(token=token).values_list('user', flat=True)
        if user_id in emailtoken:
            user = CustomUser.objects.get(id=user_id)
            user.set_password(new_password)
            user.is_verified =True
            email_token.is_active = False
            email_token.save()
            user.save()
            return response(status=status.HTTP_200_OK,message=messages.PASSWORD_RESET,data=[])
        else:
            return response(status=status.HTTP_400_BAD_REQUEST,message=messages.INVALID_TOKEN,data=[])
    except Exception as e:
        return response(status=status.HTTP_400_BAD_REQUEST,message=messages.INVALID_TOKEN,data=[])

