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

# @pytest.mark.django_db
# def test_picture_url_property_without_picture(default_station):
#     """Test that picture_url property returns None if no picture is set."""
#     assert default_station.picture_url is None


# @pytest.mark.django_db
# def test_picture_url_property_with_picture(default_station_with_relations):
#     """Test that picture_url property returns the correct URL when picture exists."""
#     assert default_station_with_relations.picture_url is not None

@pytest.mark.django_db
def test_formatted_launched_date(default_station):
    """Test that formatted_launched_date returns the correct year format."""
    expected_year = default_station.created.year
    assert default_station.formatted_launched_date == f"Since {expected_year}"

@pytest.mark.django_db
def test_station_factory_creates_valid_station():
    """
    Ensure that the StationFactory correctly creates a Station instance.
    """
    station = StationFactory()
    assert station.pk is not None

