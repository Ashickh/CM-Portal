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
    try:
        print ('Starting execution...')

        with transaction.atomic():

            feature_list = [
            {'id':1,'name':'Feature'},
            {'id':2,'name':'Roles'},
            {'id':3,'name':'Permissions'},
            {'id':4,'name':'User Management'},
            {'id':5,'name':'City'},
            {'id':6,'name':'Building'},
            {'id':7,'name':'Space'},
            ]

            roles = Role.objects.all()

            for feature in feature_list:
                if not Feature.objects.filter(id=feature['id'],name=feature['name']).exists():
                    feature = Feature.objects.create(**feature)
                    for role in roles:
                        if role.name == 'Admin':
                            RoleFeature.objects.create(role=role,feature=feature,view=True,edit=True,delete=True,create=True)
                        else:
                            RoleFeature.objects.create(role=role,feature=feature,view=False,edit=False,delete=False,create=False)

        print ('Completed execution...')



    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)




