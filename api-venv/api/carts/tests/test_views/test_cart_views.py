import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from users.tests.conftest import default_user
import logging

logger = logging.getLogger("carts")
@pytest.mark.django_db
class TestCartViewSet:

