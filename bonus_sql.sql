WITH pickup_dropoff_times AS (
    SELECT
        r.id_ride,
        r.id_driver_id,
        TO_CHAR(r.pickup_time, 'YYYY-MM') AS month,
        MAX(CASE WHEN e.description = 'Status changed to pickup' THEN e.created_at END) AS pickup_time,
        MAX(CASE WHEN e.description = 'Status changed to dropoff' THEN e.created_at END) AS dropoff_time
    FROM
        public.rides_ride r
    JOIN
        public.ride_events_rideevent e ON e.id_ride_id = r.id_ride
    GROUP BY
        r.id_ride, r.id_driver_id, TO_CHAR(r.pickup_time, 'YYYY-MM')
),
trips_over_1_hour AS (
    SELECT
        pt.*,
        EXTRACT(EPOCH FROM (pt.dropoff_time - pt.pickup_time)) AS duration_seconds
    FROM
        pickup_dropoff_times pt
    WHERE
        pt.pickup_time IS NOT NULL
        AND pt.dropoff_time IS NOT NULL
        AND (pt.dropoff_time - pt.pickup_time) > INTERVAL '1 hour'
)

SELECT
    t.month,
    CONCAT(u.first_name, ' ', u.last_name) AS driver_name,
    COUNT(*) AS trips_over_1_hour
FROM
    trips_over_1_hour t
JOIN
    public.users_user u ON u.id_user = t.id_driver_id
GROUP BY
    t.month, driver_name
ORDER BY
    t.month, driver_name;