import factory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # Generate a fake pubkey and email
    pubkey = factory.LazyFunction(generate_solana_pubkey)
    email = factory.Faker("email")
