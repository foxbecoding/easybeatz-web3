import pytest
from unittest.mock import patch, MagicMock
from rest_framework import status
from users.services import Web3LoginService

@pytest.mark.django_db
class TestWeb3LoginService:
    
