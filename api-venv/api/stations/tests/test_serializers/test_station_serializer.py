import pytest
from stations.serializers import StationSerializer
from users.tests.conftest import default_user
import logging

logger = logging.getLogger("stations")

@pytest.mark.django_db
class TestStationSerializer:
