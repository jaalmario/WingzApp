from common.base.base_viewset import BaseViewSet
from apps.users.models import User
from .serializers import BaseUserSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = BaseUserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]


class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer