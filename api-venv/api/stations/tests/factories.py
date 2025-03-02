import factory
from stations.models import Station
from users.tests.factories import UserFactory

class StationFactory(factory.django.DjangoModelFactory):
    """Factory for creating Station objects dynamically."""
    class Meta:
        model = Station

    user = factory.SubFactory(UserFactory)  # Ensure a user is created
    name = factory.Faker("company")
    handle = factory.LazyAttribute(lambda obj: obj.name.lower().replace(" ", "-"))
    email = factory.Faker("email")
