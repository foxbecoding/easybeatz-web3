from rest_framework.permissions import BasePermission
from ..models import Station

class HasStation(BasePermission):
    
    message = "Access Denied!" 

    def has_permission(self, request, view):
        found_station = Station.objects.filter(pk=str(request.user.pk)).exists()
        return found_station
