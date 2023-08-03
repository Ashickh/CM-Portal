from rest_framework import permissions
from app.space_management.models import *
from rest_framework.exceptions import PermissionDenied
from app.user_authentication.models import *

class CityPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            user = request.user
            role = UserRole.objects.get(user=user).role
            if request.method == 'GET':
                perrm = RoleFeature.objects.filter(role=role,feature__id=5,view=True)
                if perrm.exists():
                    return True
            elif request.method == 'POST':
                perrm = RoleFeature.objects.filter(role=role,feature__id=5,create=True)
                if perrm.exists():
                    return True
            elif request.method == 'PUT':
                perrm = RoleFeature.objects.filter(role=role,feature__id=5,edit=True)
                if perrm.exists():
                    return True
            elif request.method == 'DELETE':
                perrm = RoleFeature.objects.filter(role=role,feature__id=5,delete=True)
                if perrm.exists():
                    return True
            else:
                return False

        except Exception as e:
            print(e)
            return False

class BuildingPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            user = request.user
            # print(request.user)
            # print(UserRole.objects.filter(user=user))
            # return True
            role = UserRole.objects.get(user=user).role
            if request.method == 'GET':
                perrm = RoleFeature.objects.filter(role=role,feature__id=6,view=True)
                print(perrm)
                if perrm.exists():
                    return True
            elif request.method == 'POST':
                perrm = RoleFeature.objects.filter(role=role,feature__id=6,create=True)
                if perrm.exists():
                    return True
            elif request.method == 'PUT':
                perrm = RoleFeature.objects.filter(role=role,feature__id=6,edit=True)
                if perrm.exists():
                    return True
            elif request.method == 'DELETE':
                perrm = RoleFeature.objects.filter(role=role,feature__id=6,delete=True)
                if perrm.exists():
                    return True
            else:
                return False

        except Exception as e:
            return False


class RentalSpacePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            user = request.user
            role = UserRole.objects.get(user=user).role
            if request.method == 'GET':
                perrm = RoleFeature.objects.filter(role=role,feature__id=7,view=True)
                if perrm.exists():
                    return True
            elif request.method == 'POST':
                perrm = RoleFeature.objects.filter(role=role,feature__id=7,create=True)
                if perrm.exists():
                    return True
            elif request.method == 'PUT':
                perrm = RoleFeature.objects.filter(role=role,feature__id=7,edit=True)
                if perrm.exists():
                    return True
            elif request.method == 'DELETE':
                perrm = RoleFeature.objects.filter(role=role,feature__id=7,delete=True)
                if perrm.exists():
                    return True
            else:
                return False

        except:
            return False