from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Mechanic(models.Model):
    name=models.CharField(max_length=120)
    phone=models.CharField(max_length=15)
    location=models.CharField(max_length=255)
    rating=models.DecimalField(max_digits=3,decimal_places=1,default=0,
        validators=[MinValueValidator(0),MaxValueValidator(5)])
    is_open=models.BooleanField(default=True)
    services=models.JSONField(default=list)
    def __str__(self): return f"{self.name} - {self.phone}"

class ServiceRequest(models.Model):
    class Status(models.TextChoices):
        PENDING="PENDING","Pending"; ACCEPTED="ACCEPTED","Accepted"
        IN_PROGRESS="IN_PROGRESS","In Progress"; COMPLETED="COMPLETED","Completed"
        CANCELLED="CANCELLED","Cancelled"
    customer_name=models.CharField(max_length=120)
    customer_phone=models.CharField(max_length=15)
    vehicle_number=models.CharField(max_length=20)
    mechanic=models.ForeignKey(Mechanic,on_delete=models.CASCADE,related_name="service_requests")
    service=models.CharField(max_length=120)
    problem_description=models.TextField()
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.vehicle_number} - {self.service}"
