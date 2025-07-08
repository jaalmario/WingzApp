from common.base.base_viewset import BaseViewSet
from apps.ride_events.models import RideEvent
from .serializers import BaseRideEventsSerializer

class RideEventsViewset(BaseViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = BaseRideEventsSerializer
