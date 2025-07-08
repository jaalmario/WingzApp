import factory
from factory.django import DjangoModelFactory
from apps.users.models import User, UserRoles

class RiderFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"rider{n}@example.com")
    password = factory.PostGenerationMethodCall('set_password', 'RiderPass123!')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = UserRoles.RIDER
    is_deleted = False
    
class AdminFactory(RiderFactory):
    role = UserRoles.ADMIN
    
class DriverFactory(RiderFactory):
    role = UserRoles.DRIVER

class DeletedUserFactory(RiderFactory):
    is_deleted = True