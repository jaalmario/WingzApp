from rest_framework.routers import SimpleRouter
from apps.users.api.views import UserViewSet
from apps.rides.api.views import RideViewset

router = SimpleRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'rides', RideViewset, basename='rides')