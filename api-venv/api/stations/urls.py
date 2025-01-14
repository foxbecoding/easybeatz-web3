from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"station", StationViewSet, basename="station")
urlpatterns = router.urls
