from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from stations.models import StationPicture
from users.tests.conftest import default_user
import logging
from PIL import Image
import io


