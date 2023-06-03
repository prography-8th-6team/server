import logging


from django.db import close_old_connections
from rest_framework.views import exception_handler
from applications.base.response import operation_failure

logger = logging.getLogger('error')


def server_error_handler(exc, context):
    response = exception_handler(exc, context)
    if response:
        return response
    logger.exception(exc)
    logger.error(exc)
    print(exc)
    close_old_connections()
    return operation_failure
