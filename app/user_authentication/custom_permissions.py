from rest_framework import permissions
from app.user_authentication.models import *
from rest_framework.exceptions import PermissionDenied


class RolePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            user = request.user
            role = UserRole.objects.get(user=user).role
            if request.method == 'GET':
                perrm = RoleFeature.objects.filter(role=role,feature__id=2,view=True)
                if perrm.exists():
                    return True
            elif request.method == 'POST':
                perrm = RoleFeature.objects.filter(role=role,feature__id=2,create=True)
                if perrm.exists():
                    return True
            elif request.method == 'PUT':
                perrm = RoleFeature.objects.filter(role=role,feature__id=2,edit=True)
                if perrm.exists():
                    return True
            elif request.method == 'DELETE':
                perrm = RoleFeature.objects.filter(role=role,feature__id=2,delete=True)
                if perrm.exists():
                    return True
            else:
                return False

        except:
            return False

class RoleFeaturePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            user = request.user
            role = UserRole.objects.get(user=user).role
            if request.method == 'GET':
                perrm = RoleFeature.objects.filter(role=role,feature__id=3,view=True)
                if perrm.exists():
                    return True
            elif request.method == 'POST':
                perrm = RoleFeature.objects.filter(role=role,feature__id=3,create=True)
                if perrm.exists():
                    return True
            elif request.method == 'PUT':
                perrm = RoleFeature.objects.filter(role=role,feature__id=3,edit=True)
                if perrm.exists():
                    return True
            elif request.method == 'DELETE':
                perrm = RoleFeature.objects.filter(role=role,feature__id=3,delete=True)
                if perrm.exists():
                    return True
            else:
                return False

        except:
            return False


class UserManagementPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            user = request.user
            role = UserRole.objects.get(user=user).role
            if request.method == 'GET':
                perrm = RoleFeature.objects.filter(role=role,feature__id=4,view=True)
                if perrm.exists():
                    return True
            elif request.method == 'POST':
                perrm = RoleFeature.objects.filter(role=role,feature__id=4,create=True)
                if perrm.exists():
                    return True
            elif request.method == 'PUT':
                perrm = RoleFeature.objects.filter(role=role,feature__id=4,edit=True)
                if perrm.exists():
                    return True
            elif request.method == 'DELETE':
                perrm = RoleFeature.objects.filter(role=role,feature__id=4,delete=True)
                if perrm.exists():
                    return True
            else:
                return False

        except:
            return False


class CustomerManagementPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            user = request.user
            role = UserRole.objects.get(user=user).role
            if request.method == 'GET':
                perrm = RoleFeature.objects.filter(role=role,feature__id=11,view=True)
                if perrm.exists():
                    return True
            elif request.method == 'POST':
                perrm = RoleFeature.objects.filter(role=role,feature__id=11,create=True)
                if perrm.exists():
                    return True
            elif request.method == 'PUT':
                perrm = RoleFeature.objects.filter(role=role,feature__id=11,edit=True)
                if perrm.exists():
                    return True
            elif request.method == 'DELETE':
                perrm = RoleFeature.objects.filter(role=role,feature__id=11,delete=True)
                if perrm.exists():
                    return True
            else:
                return False

        except:
            return False