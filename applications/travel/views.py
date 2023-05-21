# Create your views here.
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from applications.base.response import operation_failure
from applications.travel.models import Travel
from applications.travel.serializers import TravelSerializer


class TravelViewSet(ModelViewSet):
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer

    @swagger_auto_schema(
        operation_summary="여행 전체 리스트 API",
        request_body=no_body,
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="여행 생성 API",
        request_body=no_body,
    )
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        title = data.get("title", None)
        start_date = data.get("start_date", None)
        end_date = data.get("end_date", None)

        if title and start_date and end_date:
            serializer = self.serializer_class(data=request.data, context={"request": request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                print(serializer.errors)
                return operation_failure
        else:
            return operation_failure

    @swagger_auto_schema(
        operation_summary="여행 상세 API",
        request_body=no_body,
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="여행 수정 API",
        request_body=no_body,
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="여행 삭제 탈퇴",
        request_body=no_body,
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


