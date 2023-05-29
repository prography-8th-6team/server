# Create your views here.
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from applications.base.response import operation_failure, not_found_data, delete_success, permission_error
from applications.travel.models import Travel
from applications.travel.serializers import TravelSerializer


class TravelViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer

    @swagger_auto_schema(
        operation_summary="여행 전체 리스트 API",
        request_body=no_body,
    )
    def get_object(self, pk):
        try:
            return Travel.objects.get(id=pk)
        except Travel.DoesNotExist:
            return None

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
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return operation_failure

    @swagger_auto_schema(
        operation_summary="여행 상세 API",
        request_body=no_body,
    )
    def retrieve(self, request, pk, *args, **kwargs):
        travel = self.get_object(pk)
        if not travel:
            return not_found_data

        travel_data = self.serializer_class(travel).data
        return Response(travel_data)

    @swagger_auto_schema(
        operation_summary="여행 수정 API",
        request_body=no_body,
    )
    def update(self, request, pk):
        travel = self.get_object(pk)
        if not travel:
            return not_found_data

        serializer = self.serializer_class(travel, data=request.data, partial=True)
        if serializer.is_valid():
            updated_travel = serializer.save()
            return Response(self.serializer_class(updated_travel).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="여행 삭제 탈퇴",
        request_body=no_body,
    )
    def destroy(self, request, pk, *args, **kwargs):
        travel = self.get_object(pk)
        if not travel:
            return not_found_data

        if travel.members.is_admin:
            travel.delete()
            return delete_success
        else:
            return permission_error
