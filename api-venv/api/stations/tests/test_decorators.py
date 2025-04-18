from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
import pytest
from stations.decorators import check_user_pubkey
from users.tests.conftest import default_user
from core.mixins import ResponseMixin
import logging

# Configure logging
logger = logging.getLogger("stations")

# ✅ Test View that applies the decorator
class TestView(APIView, ResponseMixin):
    @check_user_pubkey
    def get(self, request, *args, **kwargs):
        return self.view_response("Success", None, status.HTTP_200_OK)

@pytest.mark.django_db
class TestCheckUserPubkey:
    @pytest.fixture
    def factory(self):
        return APIRequestFactory()

    def test_authorized_request(self, factory, default_user):
        """Test case where the user is authorized."""
        request = factory.get('/some-endpoint/')

        # Force authentication on the request
        force_authenticate(request, user=default_user) # Simulate an authenticated user
        view = TestView.as_view()

        response = view(request, pk=default_user.pubkey)  # ✅ Matching user.pubkey

        assert response.status_code == 200
        assert response.data.get("message") == "Success"
        assert response.data.get("data") is None

    def test_unauthorized_request(self, factory, default_user):
        """Test case where the user is unauthorized."""
        request = factory.get("/some-endpoint/")

        # Force authentication on the request
        force_authenticate(request, user=default_user) # Simulate an authenticated user
        view = TestView.as_view()

        response = view(request, pk="wrong_pubkey")  # ❌ Mismatched pubkey

        assert response.status_code == 401
        assert response.data.get("message") == "Unauthorized"
        assert response.data.get("data") is None
