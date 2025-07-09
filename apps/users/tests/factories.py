import factory
from factory.django import DjangoModelFactory
from apps.users.models import User, UserRoles

class RiderFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'rider{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'RiderPass123!')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = UserRoles.RIDER
    is_deleted = False
    
class DriverFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'driver{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'DriverPass123!')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = UserRoles.DRIVER
    is_deleted = False

class AdminFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'admin{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'AdminPass123!')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = UserRoles.ADMIN
    is_deleted = False

class DeletedUserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'deleted{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'DeletedPass123!')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = UserRoles.RIDER
    is_deleted = True