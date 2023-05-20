# Create your views here.
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from applications.base.response import operation_failure
from applications.travel.models import Travel
from applications.travel.serializers import TravelSerializer


class TravelViewSet(ModelViewSet):
    queryset = Travel.objects.all()
    serializer_class = TravelSerializer

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
