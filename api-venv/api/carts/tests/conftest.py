import pytest
from django.contrib.contenttypes.models import ContentType
from users.tests.conftest import default_user
from albums.tests.conftest import default_track, default_track_price, default_track_exclusive_price
from ..models import *

# @pytest.fixture
# def default_cart(db, default_user):
#     return Cart.objects.create(user=default_user, cart_id='test-cart-123')

@pytest.fixture
def default_cart(db):
    return Cart.objects.create(cart_id='test-cart-123')

