# WingzApp
Python/Django Engineer Test

## <mark>1. Setup</mark>
1. Clone the [repository](https://github.com/jaalmario/WingzApp.git) to your local
2. run `pip -m venv env` to setup virtual env
2. run `./env/Scripts/activate`
3. run `pip install -r requirements.txt` to download dependencies
3. make sure you have the proper `.env` file (update to suit your needs)
```
    DJANGO_SETTINGS_MODULE= config.settings.local
    SECRET_KEY = django-insecure-yg)c)c+av#q+$o5o-b4+*7ik2d(n7+w#!s&x&y(4)_87xhb!^l

    DB_NAME=WingzDB
    DB_HOST=localhost
    DB_USER=postgres
    DB_PASS=postgres
    DB_PORT=5432
```
4. run `python manage.py runserver --settings=config.settings.local` (since im setting in the local env)



## <mark>2. Project Design and Structure</mark>
Based on the information I gathered from the interviewer, the company’s setup, and the public website, I opted for a modular project structure. This will allow multiple teams working in the same repo with minimal conflicts,while enabling each module to scale independently. 

Files in modules can scale to packages when needed, but I kept them simple for now. Base models are also prepared to make scaling and modifying easier.

To make development and debugging easier, I configured tools for local environments, including **drf_spectacular (Swagger)** for API documentation and testing, and **debug_toolbar** to monitor and optimize API performance and database transactions. 

*Developer notes, challenges faced, and Bonus SQL are documented at the end of the file.*
#### File Structure
    apps
    ├── rides/ (modules)
    |   ├── api/
    |   |   ├── serializers.py
    |   |   └── views.py
    |   ├── migrations/
    |   ├── tests/
    |   ├── models.py
    |   ├── apps.py
    |   ├── admin.py
    |   ├── exceptions.py
    |   ├── selectors.py
    |   └── services.py
    |
    ├── ride_events/
    └── users/
    
    common/
    ├── base/
    |   ├── base_models.py
    |   └── base_viewset.py
    ├── mixins/
    |   └── soft_delete_mixin.py
    |   
    └── utils/
        ├── pagination.py
        └── permissions.py
    
    config/
    ├── settings/
    |   └── base.py
    |   └── local.py
    ├── router.py
    └── urls.py

#### ERD
![Sample ERD](erd.png)

## <mark>3. Naming Conventions</mark>
- **Files**: snake_case → soft_delete_mixin.py
- **Classes**:
    - **Models**: PascalCase → User
    - **Serializers**: PascalCase + Serializer → UserSerializer
        - *Note: be specific on the class' purpose*
    - **Viewsets**: PascalCase + ViewSet → UserViewSet

- **Methods**: snake_case→ def annotate_rides_with_distance(self, request):
- **ColumnNames**: snake_case → is_deleted
- **Variable Names**: snake_case → new_date
- **Urls**: kebab-case → api/ride-events/
- **Constants/Env Variables**: UPPER_CASE → JWT_KEY

## <mark>4. Best Practices</mark>
- Add docstrings when necessary, especially when dealing with complex classes
    """
        Create/Modify user roles here
        Add role in the same format (CUSTOM_ROLE = 'custom_role', 'Custom Role')
    """
- Inherit from base files if applicable, to avoid repeatitions:
    class NewViewSet(BaseViewSet):
- Soft delete auditable entities
- Name the classes according to purpose to promote readablility (ex. DetailedRideSerializer)
- Use absolute imports for clarity and maintainability (avoid import * from <library>)
- Keep secrets and credentials out of version control (using .env)
- Check /swagger for api documentation

## <mark>Developer's Notes</mark>
- One of the key tasks that took most of my time was **designing the file structure** and what **code practices** that I should enforce. I have limited info on what the actual and existing team is working and practicing with. I based it with the info i gathered from the interviewer(i asked for the teams' setup), job description(looking for scalable, and maintainable; a startup), and the pubic website(for user roles). I also just mixed it with the architecture of the previous projects I have worked with. Basically blending the right amount of DRY-YAGNI-KISS(with simplified designs) and future-proof designs (scalable, testable, maintainable) to showcase my knowledge in the techstack. 
- Another specific challenge I had would be on the **GPS distance calculation**. I initially though it was a simple distance calculation between two coordinates, but after reviewing and looking for formulas for GPS, i found out it was much more complex. It also involves multiple complex functions.

## <mark>BONUS SQL</mark>

```
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
```