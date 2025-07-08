from rest_framework import serializers
from apps.rides.models import Ride
from apps.ride_events.api.serializers import BaseRideEventsSerializer
from apps.users.api.serializers import SimpleUserSerializer

class BaseRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        exclude = ['is_deleted']

    def validate(self, attrs):
        rider = attrs.get('id_rider')
        driver = attrs.get('id_driver')

        if rider and rider.is_deleted:
            raise serializers.ValidationError("Rider account is deactivated.")
        if driver and driver.is_deleted:
            raise serializers.ValidationError("Driver account is deactivated.")

        return attrs
    
class DetailedRideSerializer(BaseRideSerializer):
    id_rider = SimpleUserSerializer()
    id_driver = SimpleUserSerializer()
    