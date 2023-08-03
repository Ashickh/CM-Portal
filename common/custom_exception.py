import sys
import traceback

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import PermissionDenied
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first, 
    # to get the standard error response.

    # response = exception_handler(exc, context)

    if isinstance(exc, ObjectDoesNotExist):
        msg = str(exc)


        response = Response(
            {
                 "status": 1, 
                 "message": msg
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    elif isinstance(exc, ValidationError):
        error_messages = []
        for field, errors in exc.detail.items():
            error_messages.append({
                    'field': field,
                    'message':errors[0],
                })
        msg = error_messages

        response = Response(
            {
                 "status": 1, 
                 "message": msg
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    elif isinstance(exc, NotAuthenticated):
        print(exc)
        # error_messages = []
        # for field, errors in exc.detail.items():
        #     error_messages.append({
        #             'field': field,
        #             'message':errors[0],
        #         })
        msg = str(exc)

        response = Response(
            {
                 "status": 1, 
                 "message": msg
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    elif isinstance(exc, PermissionDenied):
        print(exc)
        # error_messages = []
        # for field, errors in exc.detail.items():
        #     error_messages.append({
        #             'field': field,
        #             'message':errors[0],
        #         })
        msg = str(exc)
       
        response = Response(
            {
                 "status": 1, 
                 "message": msg
            },
            status=status.HTTP_403_FORBIDDEN
        )
 
    else:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        err = "\n".join(traceback.format_exception(*sys.exc_info()))
        print(err)
        msg = err

        response = Response(
            {
                 "status": 1, 
                 "message": msg
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    return response


