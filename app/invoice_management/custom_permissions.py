from rest_framework import permissions
from app.invoice_management.models import *
from app.space_management.models import *
from rest_framework.exceptions import PermissionDenied
from app.user_authentication.models import *


class UtilityPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            user = request.user
            role = UserRole.objects.get(user=user).role
            if request.method == 'GET':
                perrm = RoleFeature.objects.filter(role=role,feature__id=8,view=True)
                if perrm.exists():
                    return True
            elif request.method == 'POST':
                perrm = RoleFeature.objects.filter(role=role,feature__id=8,create=True)
                print(perrm)
                if perrm.exists():
                    return True
            elif request.method == 'PUT':
                perrm = RoleFeature.objects.filter(role=role,feature__id=8,edit=True)
                if perrm.exists():
                    return True
            elif request.method == 'DELETE':
                perrm = RoleFeature.objects.filter(role=role,feature__id=8,delete=True)
                if perrm.exists():
                    return True
            else:
                return False

        except Exception as e:
            print(e,"kkkkkk")
            return False


class GrievancesPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            user = request.user
            print(user)
            role = UserRole.objects.get(user=user).role
            print(role.name)
            if request.method == 'GET':
                perrm = RoleFeature.objects.filter(role=role,feature__id=12,view=True)
                if perrm.exists():
                    return True
            elif request.method == 'POST':
                perrm = RoleFeature.objects.filter(role=role,feature__id=12,create=True)
                print(perrm)
                if perrm.exists():
                    return True
            elif request.method == 'PUT':
                perrm = RoleFeature.objects.filter(role=role,feature__id=12,edit=True)
                if perrm.exists():
                    return True
            elif request.method == 'DELETE':
                perrm = RoleFeature.objects.filter(role=role,feature__id=12,delete=True)
                if perrm.exists():
                    return True
            else:
                return False

        except Exception as e:
            print(e,"excep")
            return False