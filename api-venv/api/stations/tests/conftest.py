import pytest
from users.tests.conftest import default_user
from stations.models import Station, StationPicture
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

