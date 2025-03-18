from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..serializers import AlbumCoverEditSerializer
from ..models import Album, AlbumCover
from ..permissions import AlbumOwner
from stations.permissions import HasStation
from core.mixins import ResponseMixin
import logging

logger = logging.getLogger("albums")
