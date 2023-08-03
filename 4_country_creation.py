import os
import json
import sys
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cm_backend.settings')

import django
django.setup()

from app.space_management.models import *
from django.db import transaction

if __name__ == '__main__':
    print ('Starting country table population...')
    try:
        with transaction.atomic():

            country_list = [
                {
                'name':'India'
                }
            ]

            for country in country_list:
                country_obj = Country(
                    name=country['name']
                )
                country_obj.full_clean()
                country_obj.save()
                print ("Inserted Country ",country_obj.name)
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)