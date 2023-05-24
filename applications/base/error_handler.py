from django.db import close_old_connections
from rest_framework.views import exception_handler
from applications.base.response import operation_failure


def server_error_handler(exc, context):
    response = exception_handler(exc, context)
    if response:
        return response
    close_old_connections()
    print(exc)
    return operation_failure
