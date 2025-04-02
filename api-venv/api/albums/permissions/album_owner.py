from rest_framework.permissions import BasePermission
from ..models import Album

class AlbumOwner(BasePermission):
    
    message = "Access Denied!" 

    def has_permission(self, request, view):
        aid = view.kwargs.get("pk")
        is_owner = Album.objects.filter(aid=aid, station__user=request.user).exists()
        return is_owner

