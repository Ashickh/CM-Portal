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
            admin_role = Role.objects.filter(name='Admin')
            if admin_role.exists():
                admin_role = admin_role[0]
                print('Admin role already exist...')
            else:
                admin_role = Role.objects.create(name='Admin')
                print(admin_role.name,'created successfully...')
            # feature = Feature.objects.filter(name='Feature')
            # if feature.exists():
            #     feature = feature[0]
            #     print('feature already exist...')
            # else:
            #     feature = Feature.objects.create(name='Features')
            #     print('feature created successfully...')
            # role_feature = RoleFeature.objects.filter(role=admin_role,feature=feature)
            # if role_feature.exists():
            #     print('Feature permission already exist for admin role')
            # else:
            #     role_feature = RoleFeature.objects.create(role=admin_role,feature=feature,view=True,edit=True,delete=True,create=True)
            #     print('Feature permission added to  admin role')

            customer_role = Role.objects.filter(name='Customer')
            if customer_role.exists():
                customer_role = customer_role[0]
                print('Customer role already exist...')
            else:
                customer_role = Role.objects.create(name='Customer')
                print('Customer created successfully...')
            print ('Completed execution...')



    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)




