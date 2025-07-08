from apps.rides.models import Ride
from apps.ride_events.models import RideEvent
from django.db.models import Prefetch
from django.utils import timezone
from datetime import timedelta

def get_rides_with_recent_events():
    recent = timezone.now() - timedelta(days=1)
    recent_events_qs = RideEvent.objects.filter(created_at__gte=recent)
    return Ride.objects.select_related('id_driver', 'id_rider').prefetch_related(
        Prefetch('ride_events', queryset=recent_events_qs, to_attr='todays_ride_events')
    )