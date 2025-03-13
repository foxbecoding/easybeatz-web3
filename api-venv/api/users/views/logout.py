from django.contrib.auth import logout
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from core.mixins import ResponseMixin

class UserLogoutViewSet(viewsets.ViewSet, ResponseMixin):
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes] 

    def create(self, request):
        logout(request)
        return self.view_response("Logged out successfully", None, status.HTTP_200_OK) 
