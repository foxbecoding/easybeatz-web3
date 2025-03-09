import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from albums.models import TrackFavorite
from users.tests.conftest import default_user
import logging

logger = logging.getLogger("albums")

