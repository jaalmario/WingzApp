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
    rider = SimpleUserSerializer(source='id_rider')
    driver = SimpleUserSerializer(source='id_driver')
    todays_ride_events = BaseRideEventsSerializer(many=True, read_only=True)
    class Meta(BaseRideSerializer.Meta):
        exclude = None
        fields =['id_ride', 'rider', 'driver', 'status', 'pickup_latitude', 'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude', 'pickup_time', 'todays_ride_events']
    