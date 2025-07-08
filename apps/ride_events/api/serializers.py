from rest_framework import serializers
from apps.ride_events.models import RideEvent

class BaseRideEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        exclude= ['is_deleted']