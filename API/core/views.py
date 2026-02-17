from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Employee
from .serializers import EmployeeSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet




# Admin Login API .........


class AdminLoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(
            username=request.data["username"],
            password=request.data["password"]
        )

        if user and user.is_staff:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            })

        return Response({"error": "Invalid credentials"}, status=401)




# Dashboard API .........

class AdminDashboardAPI(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({
            "message": "Employee list access granted",
            "admin": request.user.username
        })



# Create Employee API .........

class CreateEmployeeAPI(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        email = request.data.get("email")

        if Employee.objects.filter(email=email).exists():
            return Response(
                {"error": "Employee with this email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        employee = Employee.objects.create(
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name"),
            email=email,
            phone=request.data.get("phone"),
            department=request.data.get("department"),
            designation=request.data.get("designation"),
            address=request.data.get("address"),
        )

        return Response(
            {"message": "Employee created successfully"},
            status=status.HTTP_201_CREATED
        )
    
#  View Employee Details API ...........

class EmployeeDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return None

    def get(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({"error": "Not found"}, status=404)

        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({"error": "Not found"}, status=404)

        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Employee updated successfully"})

    def delete(self, request, pk):
        employee = self.get_object(pk)
        if not employee:
            return Response({"error": "Not found"}, status=404)

        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class EmployeeListAPI(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)



# #Edit/Update Employee


# class EmployeeDetailAPI(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request, pk):
#         employee = Employee.objects.get(pk=pk)
#         serializer = EmployeeSerializer(employee)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         employee = self.get_object(pk)
#         if not employee:
#             return Response({"error": "Not found"}, status=404)

#         serializer = EmployeeSerializer(employee, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Employee updated"})
#         return Response(serializer.errors, status=400)

#     def delete(self, request, pk):
#         employee = self.get_object(pk)
#         if not employee:
#             return Response({"error": "Not found"}, status=404)

#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    


#single employee views#

class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]