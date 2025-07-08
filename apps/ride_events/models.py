from django.db import models
from common.base.base_models import AuditableModel
from apps.rides.models import Ride

class RideEvent(AuditableModel):
    """
    Model for ride events, containing AuditableModel properties
    """
    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(Ride, on_delete=models.PROTECT, related_name='ride_events')
    description = models.TextField(max_length=60)
    is_deleted = models.BooleanField(default=False)