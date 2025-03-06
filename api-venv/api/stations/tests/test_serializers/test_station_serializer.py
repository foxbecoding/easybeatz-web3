import pytest
from stations.serializers import StationSerializer
from users.tests.conftest import default_user
import logging

logger = logging.getLogger("stations")

@pytest.mark.django_db
class TestStationSerializer:
    @pytest.fixture
    def user(self, default_user):
        return default_user

    @pytest.fixture
    def station(self, default_station):
        return default_station

