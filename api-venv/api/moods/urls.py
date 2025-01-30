from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"mood", MoodViewSet, basename="mood")
urlpatterns = router.urls
