from rest_framework.routers import SimpleRouter
from apps.users.api.views import UserViewSet
from apps.rides.api.views import RideViewset
from apps.ride_events.api.views import RideEventsViewset

router = SimpleRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'rides', RideViewset, basename='rides')
router.register(r'ride-events', RideEventsViewset, basename='ride-events')