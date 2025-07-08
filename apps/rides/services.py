from django.db.models import F, FloatField, ExpressionWrapper, Func, Value
from math import radians

def annotate_rides_with_distance(queryset, latitude, longitude):
    """
    Follow Haversine Formula to calculate distance between two GPS coordinates
    """
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        raise ValueError("Invalid coordinates provided.")

    return queryset.annotate(
        distance=ExpressionWrapper(
            6371 * Func(
                Func(
                    Func(
                        Value(latitude), function='RADIANS'
                    ) - Func(F('pickup_latitude'), function='RADIANS'),
                    function='SIN'
                ) ** 2
                +
                Func(
                    Func(Value(longitude), function='RADIANS') - Func(F('pickup_longitude'), function='RADIANS'),
                    function='SIN'
                ) ** 2
                * Func(
                    Func(Value(latitude), function='RADIANS'),
                    function='COS'
                )
                * Func(
                    Func(F('pickup_latitude'), function='RADIANS'),
                    function='COS'
                ),
                function='SQRT'
            ),
            output_field=FloatField()
        )
    )