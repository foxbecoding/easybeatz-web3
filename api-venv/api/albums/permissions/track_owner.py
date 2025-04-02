from rest_framework.permissions import BasePermission
from ..models import Track

class TrackOwner(BasePermission):
    
    message = "Access Denied!" 

    def has_permission(self, request, view):
        tid = view.kwargs.get("pk")
        is_track_owner = Track.objects.filter(album__station__user=request.user, tid=tid).exists()
        return is_track_owner

