from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from ..models import UserLogin 

class UserLoginViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving user logins.
    """
    def list(self, request):
        return Response("fox")
