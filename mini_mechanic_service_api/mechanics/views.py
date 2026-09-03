from rest_framework import viewsets,filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Mechanic,ServiceRequest
from .serializers import MechanicSerializer,ServiceRequestSerializer
from .permissions import IsAdminOrReadOnly

class MechanicViewSet(viewsets.ModelViewSet):
    queryset=Mechanic.objects.all().order_by("id")
    serializer_class=MechanicSerializer
    permission_classes=[IsAdminOrReadOnly]
    filter_backends=[DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields=["is_open","location"]
    search_fields=["name","location","services"]
    ordering_fields=["id","name","rating"]

class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset=ServiceRequest.objects.select_related("mechanic").all().order_by("-created_at")
    serializer_class=ServiceRequestSerializer
    permission_classes=[AllowAny]
    filter_backends=[DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields=["status","mechanic"]
    search_fields=["customer_name","customer_phone","vehicle_number","service"]
    ordering_fields=["created_at","status"]
