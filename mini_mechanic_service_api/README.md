# Mini Mechanic Service API

Django + Django REST Framework assignment implementation.

## Run locally

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API: http://127.0.0.1:8000
Swagger: http://127.0.0.1:8000/api/docs/
Admin: http://127.0.0.1:8000/admin/

## JWT

POST `/api/auth/token/`
```json
{"username":"adminuser","password":"StrongPass123"}
```
Use `Authorization: Bearer <access>` for mechanic create/update/delete.

## Endpoints

GET/POST `/api/mechanics/`
GET/PUT/PATCH/DELETE `/api/mechanics/<id>/`
GET/POST `/api/service-requests/`
GET/PUT/PATCH/DELETE `/api/service-requests/<id>/`

Search/filter examples:
`/api/mechanics/?search=Raj`
`/api/mechanics/?location=Ahmedabad`
`/api/mechanics/?is_open=true`
`/api/mechanics/?ordering=-rating`
`/api/mechanics/?page=2&page_size=5`

## Create mechanic
```json
{"name":"Raj Auto Care","phone":"9876543210","location":"Ahmedabad","rating":4.5,"is_open":true,"services":["Oil Change","Brake Repair","Engine Repair"]}
```

## Create service request
```json
{"customer_name":"Amit Sharma","customer_phone":"9876543212","vehicle_number":"GJ01AB1234","mechanic_id":1,"service":"Oil Change","problem_description":"Engine oil needs replacement"}
```

## Tests
`python manage.py test`

## Docker/PostgreSQL
`docker compose up --build`
