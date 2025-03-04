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

# ✅ Test View that applies the decorator
class TestView(APIView):
    @check_user_pubkey
    def get(self, request, *args, **kwargs):
        return Response({"message": "Success"}, status=status.HTTP_200_OK)

@pytest.mark.django_db
class TestCheckUserPubkey:
    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

