from django.db import models
from apps.users.models import User

class RideStatus(models.TextChoices):
    """
    Create/Modify RideStatus here
    Add status in the same format (CUSTOM_STATUS = 'custom_status', 'Custom Status')
    """
    EN_ROUTE = 'en-route', 'En-route'
    PICKUP = 'pickup', 'Pickup'
    DROPOFF = 'dropoff', 'Dropoff'

class Ride(models.Model):
    """
    Ride model representing different roles in the application.
    """
    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=RideStatus, default=RideStatus.EN_ROUTE)
    
    id_rider = models.ForeignKey(
        User,
        related_name='rides_as_rider',
        on_delete=models.PROTECT
    )
    id_driver = models.ForeignKey(
        User,
        related_name='rides_as_driver',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)