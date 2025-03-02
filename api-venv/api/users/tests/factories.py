import factory
import uuid
from users.models import User, UserLogin, UserLoginNonce

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # Generate a fake pubkey and email
    pubkey = factory.LazyFunction(generate_solana_pubkey)
    email = factory.Faker("email")
