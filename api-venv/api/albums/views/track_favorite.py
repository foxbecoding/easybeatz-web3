from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from albums.serializers import TrackFavoriteSerializer
from albums.models import Track

