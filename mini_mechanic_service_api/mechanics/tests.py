from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Mechanic

class APITests(APITestCase):
    def setUp(self):
        self.mechanic=Mechanic.objects.create(name="Raj Auto Care",phone="9876543210",location="Ahmedabad",rating=4.5,is_open=True,services=["Oil Change","Brake Repair"])
        self.user=get_user_model().objects.create_user(username="adminuser",password="StrongPass123")
    def test_list(self):
        r=self.client.get("/api/mechanics/"); self.assertEqual(r.status_code,200)
    def test_service_request(self):
        r=self.client.post("/api/service-requests/",{"customer_name":"Amit","customer_phone":"9876543212","vehicle_number":"GJ01AB1234","mechanic_id":self.mechanic.id,"service":"Oil Change","problem_description":"Oil replacement"},format="json")
        self.assertEqual(r.status_code,201); self.assertEqual(r.data["status"],"PENDING")
    def test_invalid_phone(self):
        r=self.client.post("/api/service-requests/",{"customer_name":"Amit","customer_phone":"123","vehicle_number":"GJ01AB1234","mechanic_id":self.mechanic.id,"service":"Oil Change","problem_description":"Test"},format="json")
        self.assertEqual(r.status_code,400)
    def test_create_mechanic_auth(self):
        r=self.client.post("/api/mechanics/",{"name":"New","phone":"9876543211","location":"Ahmedabad","rating":4,"is_open":True,"services":["Oil Change"]},format="json")
        self.assertEqual(r.status_code,401)
        self.client.force_authenticate(self.user)
        r=self.client.post("/api/mechanics/",{"name":"New","phone":"9876543211","location":"Ahmedabad","rating":4,"is_open":True,"services":["Oil Change"]},format="json")
        self.assertEqual(r.status_code,201)
