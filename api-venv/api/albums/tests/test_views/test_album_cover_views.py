import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from albums.models import Album, Track
from stations.tests.conftest import default_station, default_station_picture
from users.tests.conftest import default_user
import logging

logger = logging.getLogger("albums")
