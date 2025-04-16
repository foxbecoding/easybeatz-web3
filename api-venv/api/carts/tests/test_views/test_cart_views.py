import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from users.tests.conftest import default_user
from genres.tests.conftest import default_genre
from moods.tests.conftest import default_mood
from stations.tests.conftest import default_station, default_station_picture
from albums.tests.conftest import default_album, default_album_cover, default_track, default_track_price, default_track_exclusive_price, default_track_display, test_mp3_file, test_img_file
from carts.models import *
import logging

logger = logging.getLogger("carts")
@pytest.mark.django_db
class TestCartViewSet:

    @pytest.fixture
    def client(self):
        settings.SECURE_SSL_REDIRECT = False  # Disable automatic redirect to HTTPS
        return APIClient()

    @pytest.fixture
    def user(self, default_user):
        """Fixture to create a test user with a public key."""
        return default_user

    @pytest.fixture
    def station(self, default_station):
        return default_station

    @pytest.fixture
    def station_picture(self, default_station_picture):
        return default_station_picture

    @pytest.fixture
    def album(self, default_album):
        return default_album

    @pytest.fixture
    def album_cover(self, default_album_cover):
        return default_album_cover

    @pytest.fixture
    def track(self, default_track):
        return default_track

    @pytest.fixture
    def track_display(self, default_track_display):
        return default_track_display

    @pytest.fixture
    def track_price(self, default_track_price):
        return default_track_price

    @pytest.fixture
    def track_exclusive_price(self, default_track_exclusive_price):
        return default_track_exclusive_price

    @pytest.fixture
    def genre(self, default_genre):
        return default_genre

    @pytest.fixture
    def mood(self, default_mood):
        return default_mood

    @pytest.fixture
    def cart(self, default_cart):
        return default_cart

    @pytest.fixture
    def cart_item(self, default_cart_item):
        return default_cart_item

    @pytest.fixture
    def cart_item_exclusive(self, default_cart_item_exclusive):
        return default_cart_item_exclusive

    @pytest.fixture
    def request_data_track_price(self, track):
        return {
            "tid": track.tid,
            "type": "TRACK_PRICE"
        }

    @pytest.fixture
    def request_data_track_exclusive_price(self, track):
        return {
            "tid": track.tid,
            "type": "TRACK_EXCLUSIVE_PRICE"
        } 

    @pytest.fixture
    def invalid_request_data_tid(self):
        return {
            "tid": "wrong_tid",
            "type": "TRACK_PRICE"
        }

    @pytest.fixture
    def invalid_request_data_type(self, track):
        return {
            "tid": track.tid,
            "type": "WRONG_TYPE"
        }


    @pytest.mark.django_db
    def test_get_cart_view(self, db, client, user, station, station_picture, cart, cart_item, cart_item_exclusive, album, album_cover, track, track_display, track_price, track_exclusive_price, genre, mood):
        # Set the cookie before making the request
        client.cookies['cart_id'] = cart.cart_id
        url = reverse("cart-get-cart")
        response = client.get(url)

        cart_subtotal = track_price.value + track_exclusive_price.value

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get("message") is None 
        assert "items" in response.data.get("data")
        assert response.data.get("data").get("cart_count") == 2
        assert response.data.get("data").get("cart_subtotal") == cart_subtotal

    @pytest.mark.django_db
    def test_add_cart_item_view(
            self, 
            db, 
            client, 
            user, 
            station,
            station_picture,
            cart, 
            album,
            album_cover,
            track, 
            track_display,
            track_price, 
            track_exclusive_price, 
            genre, 
            mood, 
            request_data_track_price):
        # Set the cookie before making the request
        client.cookies['cart_id'] = cart.cart_id
        url = reverse("cart-add-cart-item")
        request_data = request_data_track_price
        response = client.post(url, request_data )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("message") == "Track added to cart"
        assert response.data.get("data") != []

        price_model_ct = ContentType.objects.get_for_model(track_price)
        cart_item = CartItem.objects.filter(
            cart__cart_id=cart.cart_id, 
            track__tid=request_data["tid"], 
            price_model_type=price_model_ct, 
            price_model_id=track_price.pk
        ).exists()
        assert cart_item == True

    @pytest.mark.django_db
    def test_add_cart_item_authenticated_view(self, db, client, user, station, station_picture, album, album_cover, track, track_display, track_price, track_exclusive_price, genre, mood, request_data_track_price):
        client.force_authenticate(user=user)
        # Set the cookie before making the request
        cart_id = "cart-test-id-111"
        client.cookies['cart_id'] = cart_id
        url = reverse("cart-add-cart-item")
        request_data = request_data_track_price
        response = client.post(url, request_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("message") == "Track added to cart"
        assert response.data.get("data") != []

        price_model_ct = ContentType.objects.get_for_model(track_price)
        cart_item = CartItem.objects.filter(
            cart__cart_id=cart_id,
            track__tid=request_data["tid"], 
            price_model_type=price_model_ct, 
            price_model_id=track_price.pk
        ).exists()
        assert cart_item == True

    @pytest.mark.django_db
    def test_add_cart_item_exclusive_view(self, db, client, user, station, station_picture, cart, album, album_cover, track, track_display, track_price, track_exclusive_price, genre, mood, request_data_track_exclusive_price):
        # Set the cookie before making the request
        client.cookies['cart_id'] = cart.cart_id
        url = reverse("cart-add-cart-item")
        request_data = request_data_track_exclusive_price
        response = client.post(url, request_data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get("message") == "Track added to cart"
        assert response.data.get("data") != []

        price_model_ct = ContentType.objects.get_for_model(track_exclusive_price)
        cart_item = CartItem.objects.filter(
            cart__cart_id=cart.cart_id, 
            track__tid=request_data["tid"], 
            price_model_type=price_model_ct, 
            price_model_id=track_exclusive_price.pk
        ).exists()
        assert cart_item == True

    @pytest.mark.django_db
    def test_add_cart_item_view_invalid_tid_error(self, db, client, user, station, station_picture, cart, album, album_cover, track, track_display, track_price, track_exclusive_price, genre, mood, invalid_request_data_tid):
        # Set the cookie before making the request
        client.cookies['cart_id'] = cart.cart_id
        url = reverse("cart-add-cart-item")
        request_data = invalid_request_data_tid
        response = client.post(url, request_data )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("message") == "Track not found"
        assert response.data.get("data") is None


    @pytest.mark.django_db
    def test_add_cart_item_view_invalid_type_error(self, db, client, user, station, station_picture, cart, album, album_cover, track, track_display, track_price, track_exclusive_price, genre, mood, invalid_request_data_type):
        # Set the cookie before making the request
        client.cookies['cart_id'] = cart.cart_id
        url = reverse("cart-add-cart-item")
        request_data = invalid_request_data_type
        response = client.post(url, request_data )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data.get("message") == "Invalid track pricing type"
        assert response.data.get("data") is None 

