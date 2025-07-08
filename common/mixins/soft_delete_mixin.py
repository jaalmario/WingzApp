from rest_framework.response import Response
from rest_framework import status

class SoftDeleteMixin:
    """
    Soft delete the instance by setting `is_deleted = True` instead of actually deleting it.
    """
    def destroy(self, request,*args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)