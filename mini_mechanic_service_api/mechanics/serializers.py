import re
from rest_framework import serializers
from .models import Mechanic, ServiceRequest
PHONE_RE=re.compile(r"^\+?[0-9]{10,13}$")
VEHICLE_RE=re.compile(r"^[A-Z]{2}[ -]?[0-9]{1,2}[ -]?[A-Z]{1,3}[ -]?[0-9]{1,4}$")

class MechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mechanic
        fields=["id","name","phone","location","rating","is_open","services"]
    def validate_phone(self,value):
        value=value.strip()
        if not PHONE_RE.fullmatch(value): raise serializers.ValidationError("Enter a valid phone number.")
        return value
    def validate_services(self,value):
        if not isinstance(value,list) or not value: raise serializers.ValidationError("services must be a non-empty list.")
        if not all(isinstance(x,str) and x.strip() for x in value): raise serializers.ValidationError("Each service must be a non-empty string.")
        return [x.strip() for x in value]

class ServiceRequestSerializer(serializers.ModelSerializer):
    mechanic_id=serializers.PrimaryKeyRelatedField(source="mechanic",queryset=Mechanic.objects.all(),write_only=True)
    mechanic=MechanicSerializer(read_only=True)
    class Meta:
        model=ServiceRequest
        fields=["id","customer_name","customer_phone","vehicle_number","mechanic_id","mechanic","service","problem_description","status","created_at"]
        read_only_fields=["id","mechanic","status","created_at"]
    def validate_customer_phone(self,value):
        value=value.strip()
        if not PHONE_RE.fullmatch(value): raise serializers.ValidationError("Enter a valid customer phone number.")
        return value
    def validate_vehicle_number(self,value):
        value=value.strip().upper()
        if not VEHICLE_RE.fullmatch(value): raise serializers.ValidationError("Enter a valid vehicle number, e.g. GJ01AB1234.")
        return value
    def validate(self,attrs):
        mechanic=attrs["mechanic"]; service=attrs["service"].strip()
        if not mechanic.is_open: raise serializers.ValidationError({"mechanic_id":"This mechanic is currently closed."})
        if service.lower() not in [x.strip().lower() for x in mechanic.services]:
            raise serializers.ValidationError({"service":f"Invalid service. Available services: {mechanic.services}"})
        attrs["service"]=service
        return attrs
