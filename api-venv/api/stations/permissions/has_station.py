from rest_framework.permissions import BasePermission
from ..models import Station
from users.models import User

class HasStation(BasePermission):
    
    message = "Access Denied!" 

    def has_permission(self, request, view) -> bool:
        user = User.objects.filter(pubkey=str(request.user)).first()
        station = Station.objects.filter(pk=user.pk).first()
        if not station:
            return False
        return True
