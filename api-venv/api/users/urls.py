from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"web3-login", UserLoginViewSet, basename="web3-login")
urlpatterns = router.urls
