from django.urls import path

from .views import (AdminLoginAPI, AdminDashboardAPI,  EmployeeListAPI, CreateEmployeeAPI, EmployeeDetailAPI)

urlpatterns = [
    path('admin/login/', AdminLoginAPI.as_view()),
    path('admin/dashboard/', AdminDashboardAPI.as_view()),
    path('admin/create-employee/', CreateEmployeeAPI.as_view()),
    path('admin/employees/', EmployeeListAPI.as_view()),
    path('admin/employees/<int:pk>/', EmployeeDetailAPI.as_view()),  
]










# {
#   "username": "admin",
#   "password": "adm@1234"
# }


# {
#   "first_name": "John",
#   "last_name": "Doe",
#   "email": "john.doe@gmail.com",
#   "phone": "9876543210",
#   "department": "IT",
#   "designation": "Software Engineer",
#   "address": "Delhi, India"
# }
