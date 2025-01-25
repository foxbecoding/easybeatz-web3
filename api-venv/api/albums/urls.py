from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"album", AlbumViewSet, basename="album")
router.register(r"album-project", AlbumProjectViewSet, basename="album_project")
router.register(r"track", TrackViewSet, basename="track")
urlpatterns = router.urls
