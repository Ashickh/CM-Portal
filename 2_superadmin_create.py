


import os
import json
import sys
import traceback
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cm_backend.settings')

import django
django.setup()

from app.user_authentication.models import *
from django.db import transaction

if __name__ == '__main__':
    print ('Starting execution...')
    try:
        with transaction.atomic():
            email='admin@getnada.com'
            password='admin@123'
            phonenumber='8080080808'
            first_name='Super'
            last_name='Admin'
            address='nil'
            superadmin = CustomUser(first_name=first_name,
                last_name=last_name,
                email=email,
                phonenumber=phonenumber,
                is_superuser=True,
                is_staff=True,
                address=address,
                is_verified=True)
            superadmin.set_password(password)
            superadmin.full_clean()
            superadmin.save()

            admin_role = Role.objects.get(name='Admin')

            user_role_obj = UserRole(user=superadmin,role=admin_role)
            user_role_obj.full_clean()
            user_role_obj.save()

            print ('Completed execution...')



    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
