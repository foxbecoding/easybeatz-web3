from django.contrib.auth import logout
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class UserLogoutViewSet(viewsets.ViewSet):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes] 

    def create(self, request):
        logout(request)
        return Response(None, status=status.HTTP_200_OK) 
