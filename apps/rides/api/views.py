from common.base.base_viewset import BaseViewSet
from apps.rides.models import Ride
from .serializers import BaseRideSerializer

class RideViewset(BaseViewSet):
    queryset = Ride.objects.all()
    serializer_class = BaseRideSerializer