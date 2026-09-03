from rest_framework.routers import DefaultRouter
from .views import MechanicViewSet,ServiceRequestViewSet
router=DefaultRouter()
router.register("mechanics",MechanicViewSet,basename="mechanic")
router.register("service-requests",ServiceRequestViewSet,basename="service-request")
urlpatterns=router.urls
