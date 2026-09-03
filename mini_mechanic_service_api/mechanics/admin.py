from django.contrib import admin
from .models import Mechanic,ServiceRequest
@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):
    list_display=("id","name","phone","location","rating","is_open")
    search_fields=("name","phone","location")
    list_filter=("is_open",)
@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display=("id","customer_name","vehicle_number","mechanic","service","status","created_at")
    search_fields=("customer_name","vehicle_number","customer_phone")
    list_filter=("status",)
