from rest_framework.response import Response

operation_success = Response(status=200, data={"message": "OPERATION_SUCCESS"})
operation_failure = Response(status=400, data={"message": "OPERATION_FAILURE"})

certification_failure = Response(status=401, data={'message': 'CERTIFICATION_FAILURE'})