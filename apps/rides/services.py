from django.db.models import F, FloatField, ExpressionWrapper, Func, Value
from math import radians

def annotate_rides_with_distance(queryset, latitude, longitude):
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        raise ValueError("Invalid coordinates provided.")

    return queryset.annotate(
        distance=ExpressionWrapper(
            6371 * Func(
                Func(
                    Func(F('pickup_latitude'), function='RADIANS'),
                    function='COS'
                ) * Func(
                    Value(latitude),
                    function='COS'
                ) * Func(
                    Func(F('pickup_longitude') - Value(longitude), function='RADIANS'),
                    function='COS'
                ) + Func(
                    Func(F('pickup_latitude'), function='RADIANS'),
                    function='SIN'
                ) * Func(
                    Value(latitude),
                    function='SIN'
                ),
                function='ACOS'
            ),
            output_field=FloatField()
        )
    )