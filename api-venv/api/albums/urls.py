from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"album", AlbumViewSet, basename="album")
router.register(r"album-cover", AlbumCoverViewSet, basename="album-cover")
router.register(r"track", TrackViewSet, basename="track")
router.register(r"track-price", TrackPriceViewSet, basename="track-price")
router.register(r"track-exclusive-price", TrackExclusivePriceViewSet, basename="track-exclusive-price")
router.register(r"track-favorite", TrackFavoriteViewSet, basename="track-favorite")
urlpatterns = router.urls
