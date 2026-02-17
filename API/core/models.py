from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)

    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)

    address = models.TextField(blank=True)

    # profile_photo = models.ImageField(
    #     upload_to='employees/profile_photos/',
    #     blank=True,
    #     null=True
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

