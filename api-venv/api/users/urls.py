from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"user-login", UserLoginViewSet, basename="user-login")
urlpatterns = router.urls
