import os
import json
import sys
import traceback
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cm_backend.settings')

import django
django.setup()

from app.space_management.models import *
from django.db import transaction

if __name__ == '__main__':
    print ('Starting country table population...')
    try:
        with transaction.atomic():

            country = Country.objects.get(name='India',is_active=True)

            with open('india_states.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    state_name = row[0]
                    state_obj = State(
                        name = state_name,
                        country = country
                    )
                    state_obj.full_clean()
                    state_obj.save()
                    print ("Inserted State ",state_obj.name)

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)




