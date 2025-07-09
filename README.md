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
