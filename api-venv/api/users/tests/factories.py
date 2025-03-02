import factory
import uuid
from users.models import User, UserLogin, UserLoginNonce

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # Generate a fake pubkey and email
    pubkey = factory.Faker("bothify", text="#" * 44)
    email = factory.Faker("email")
    created = factory.Faker("date_time_this_decade")
    updated = factory.Faker("date_time_this_decade")
    deleted = None

class UserLoginFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserLogin

    user = factory.SubFactory(UserFactory)
    created = factory.Faker("date_time_this_decade")
    updated = factory.Faker("date_time_this_decade")
    deleted = None

