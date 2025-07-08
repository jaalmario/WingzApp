from common.base.base_viewset import BaseViewSet
from apps.rides.models import Ride
from .serializers import BaseRideSerializer, DetailedRideSerializer
from apps.rides.services import annotate_rides_with_distance
from apps.rides.exceptions import CoordinatesNotFound
from drf_spectacular.utils import extend_schema, OpenApiParameter
from apps.ride_events.api.views import BaseRideEventsSerializer

class RideViewset(BaseViewSet):
    queryset = Ride.objects.all()
    serializer_class = BaseRideSerializer
    filterset_fields = ['status', 'id_rider__email']
    ordering_fileds = ['pickup_time', 'distance']
    serializer_action_classes = {
        'list': DetailedRideSerializer
    }

    def get_serializer_class(self):
        return self.serializer_action_classes.get(self.action, BaseRideEventsSerializer )

    def get_queryset(self):
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        ordering = self.request.query_params.get('ordering')
        
        qs = self.queryset

        if ordering == 'distance' or ordering == '-distance':
            if not (latitude and longitude):
                raise CoordinatesNotFound()
            qs = annotate_rides_with_distance(queryset=qs, latitude=latitude, longitude=longitude)
            
            if ordering == "distance":
                qs = qs.order_by("distance")
            elif ordering == "-distance":
                qs = qs.order_by("-distance")

        return qs
    
    @extend_schema(parameters=[
        OpenApiParameter(name='latitude', description='if filter is distance, requires latitude and longitude', type=float),
        OpenApiParameter(name='longitude', description='if filter is distance, requires latitude and longitude', type=float),
        ])
    def list(self, request):
        return super().list(request=request)