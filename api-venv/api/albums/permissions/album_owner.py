from rest_framework.permissions import BasePermission
from ..models import Album
from stations.models import Station

class AlbumOwner(BasePermission):
    
    message = "Access Denied!" 

    def has_permission(self, request, view):
        aid = view.kwargs.get("pk")
        station = Station.objects.get(user=request.user)
        is_owner = Album.objects.filter(aid=aid, station=station).exists()
        return is_owner

