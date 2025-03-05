
import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from stations.models import Station
from users.tests.conftest import default_user
from albums.tests.conftest import default_album, default_album_cover, default_track
from django.conf import settings
import logging

logger = logging.getLogger("stations")
