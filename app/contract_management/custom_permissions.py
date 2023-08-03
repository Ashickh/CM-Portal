from rest_framework import permissions
from app.user_authentication.models import *
from rest_framework.exceptions import PermissionDenied


class SpaceRequestPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            user = request.user
            role = UserRole.objects.get(user=user).role
            if request.method == 'GET':
                perrm = RoleFeature.objects.filter(role=role,feature__id=9,view=True)
                if perrm.exists():
                    return True
            elif request.method == 'POST':
                perrm = RoleFeature.objects.filter(role=role,feature__id=9,create=True)
                if perrm.exists():
                    return True
            elif request.method == 'PUT':
                perrm = RoleFeature.objects.filter(role=role,feature__id=9,edit=True)
                if perrm.exists():
                    return True
            elif request.method == 'DELETE':
                perrm = RoleFeature.objects.filter(role=role,feature__id=9,delete=True)
                if perrm.exists():
                    return True
            else:
                return False

        except:
            return False

class ContractPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            user = request.user
            role = UserRole.objects.get(user=user).role
            if request.method == 'GET':
                perrm = RoleFeature.objects.filter(role=role,feature__id=10,view=True)
                if perrm.exists():
                    return True
            elif request.method == 'POST':
                perrm = RoleFeature.objects.filter(role=role,feature__id=10,create=True)
                if perrm.exists():
                    return True
            elif request.method == 'PUT':
                perrm = RoleFeature.objects.filter(role=role,feature__id=10,edit=True)
                if perrm.exists():
                    return True
            elif request.method == 'DELETE':
                perrm = RoleFeature.objects.filter(role=role,feature__id=10,delete=True)
                if perrm.exists():
                    return True
            else:
                return False

        except:
            return False

