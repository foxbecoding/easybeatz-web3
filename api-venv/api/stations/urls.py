from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"station", StationViewSet, basename="station")
router.register(r"station-picture", StationPictureViewSet, basename="station-picture")
urlpatterns = router.urls
