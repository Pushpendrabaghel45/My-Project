from django.db import migrations,models
import django.core.validators
import django.db.models.deletion
class Migration(migrations.Migration):
    initial=True; dependencies=[]
    operations=[
      migrations.CreateModel(name="Mechanic",fields=[
        ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
        ("name",models.CharField(max_length=120)),("phone",models.CharField(max_length=15)),
        ("location",models.CharField(max_length=255)),("rating",models.DecimalField(decimal_places=1,default=0,max_digits=3,validators=[django.core.validators.MinValueValidator(0),django.core.validators.MaxValueValidator(5)])),
        ("is_open",models.BooleanField(default=True)),("services",models.JSONField(default=list))]),
      migrations.CreateModel(name="ServiceRequest",fields=[
        ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
        ("customer_name",models.CharField(max_length=120)),("customer_phone",models.CharField(max_length=15)),
        ("vehicle_number",models.CharField(max_length=20)),("service",models.CharField(max_length=120)),
        ("problem_description",models.TextField()),("status",models.CharField(choices=[("PENDING","Pending"),("ACCEPTED","Accepted"),("IN_PROGRESS","In Progress"),("COMPLETED","Completed"),("CANCELLED","Cancelled")],default="PENDING",max_length=20)),
        ("created_at",models.DateTimeField(auto_now_add=True)),
        ("mechanic",models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name="service_requests",to="mechanics.mechanic"))])
    ]
