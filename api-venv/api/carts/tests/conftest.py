import pytest
from django.contrib.contenttypes.models import ContentType
from users.tests.conftest import default_user
from albums.tests.conftest import default_track, default_track_price, default_track_exclusive_price
from ..models import *

