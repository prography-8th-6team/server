from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

operation_success = Response(status=status.HTTP_200_OK, data={"message": "OPERATION_SUCCESS"})
operation_failure = Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "OPERATION_FAILURE"})

delete_success = Response(status=status.HTTP_204_NO_CONTENT, data={"message": "DELETE_SUCCESS"})
not_found_data = Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "NOT_FOUND_DATA"})
certification_failure = Response(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'CERTIFICATION_FAILURE'})
permission_error = Response(status=status.HTTP_403_FORBIDDEN, data={'message': 'PERMISSION_ERROR'})

# middleware error
authorization_error = JsonResponse(status=status.HTTP_401_UNAUTHORIZED, data={'message': 'AUTHORIZATION_ERROR'})
expired_token = JsonResponse(status=status.HTTP_403_FORBIDDEN, data={'message': 'EXPIRED_TOKEN'})
