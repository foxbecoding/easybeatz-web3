from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"genre", GenreViewSet, basename="genre")
urlpatterns = router.urls
