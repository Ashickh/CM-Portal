import sys
import traceback
from rest_framework.response import Response
from rest_framework import status

# Response structure

def responce(status,message,data):
    res = {"status":status,"message":message,"data":data}
    return Response(res)

def success_response(status, message, data):
    return Response(
        {
             "status": 0, 
             "message": message, 
              "data": data
        },
        status=status
    )

def failure_response(status, message, data):
    return Response(
        {
             "status": 1, 
             "message": message, 
              "data": data
        },
        status=status
    )

def error_response():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    err = "\n".join(traceback.format_exception(*sys.exc_info()))
    print(err)
    return Response(
        {
             "status": 1, 
             "message": err
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

def format_validation_error(e):
    error_messages = []
    for field, errors in e.detail.items():
        error_messages.append({
                'field': field,
                'message':errors[0],
            })
    # print(error_messages)
    return error_messages  

def validation_error_response(e):
    error_messages = format_validation_error(e)
    print(error_messages)
    return Response(
        {
             "status": 1, 
             "message": error_messages
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )