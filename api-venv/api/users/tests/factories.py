import factory
def generate_solana_pubkey():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=44))

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    # Generate a fake pubkey and email
    pubkey = factory.LazyFunction(generate_solana_pubkey)
    email = factory.Faker("email")
