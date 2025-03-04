from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
import pytest
from stations.decorators import check_user_pubkey
from users.tests.conftest import default_user
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

