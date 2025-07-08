from rest_framework import viewsets
from common.mixins.soft_delete_mixin import SoftDeleteMixin
from common.utils.permissions import IsAdminPermission
from common.utils.pagination import BasePagination

class BaseViewSet(SoftDeleteMixin, viewsets.ModelViewSet):
    """
    Base viewset that provides basic and standard fucntionality for all viewsets.
    It inclides pagination, soft delete functionality, and basic permissions.
    """
    permission_classes = [IsAdminPermission]
    pagination_class = BasePagination

    def get_queryset(self):
        return self.queryset.filter(is_deleted=False)