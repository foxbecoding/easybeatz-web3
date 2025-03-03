import pytest
from users.tests.conftest import default_user
from stations.models import Station, StationPicture
from stations.tests.factories import StationFactory

@pytest.mark.django_db
def test_station_create(db, default_user):
    """ 
    Ensure a Station model can be created successfully.
    """
    station = Station.objects.create(
        user=default_user,
        name="Test Station",
        handle="teststation",
        description="This is a test station.",
        email="station@example.com",
    )

    assert station.pk is not None

