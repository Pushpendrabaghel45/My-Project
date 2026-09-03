from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-change-me")
DEBUG = os.getenv("DEBUG", "1") == "1"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
INSTALLED_APPS = [
    "django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
    "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles",
    "rest_framework","django_filters","drf_spectacular","mechanics",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware","django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[],"APP_DIRS":True,
"OPTIONS":{"context_processors":["django.template.context_processors.request","django.contrib.auth.context_processors.auth",
"django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
if os.getenv("DB_ENGINE","sqlite3") == "postgresql":
    DATABASES={"default":{"ENGINE":"django.db.backends.postgresql","NAME":os.getenv("POSTGRES_DB","mechanic_db"),
    "USER":os.getenv("POSTGRES_USER","mechanic_user"),"PASSWORD":os.getenv("POSTGRES_PASSWORD","mechanic_password"),
    "HOST":os.getenv("POSTGRES_HOST","db"),"PORT":os.getenv("POSTGRES_PORT","5432")}}
else:
    DATABASES={"default":{"ENGINE":"django.db.backends.sqlite3","NAME":BASE_DIR/"db.sqlite3"}}
AUTH_PASSWORD_VALIDATORS=[]
LANGUAGE_CODE="en-us"; TIME_ZONE="Asia/Kolkata"; USE_I18N=True; USE_TZ=True
STATIC_URL="static/"
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
REST_FRAMEWORK={
"DEFAULT_AUTHENTICATION_CLASSES":("rest_framework_simplejwt.authentication.JWTAuthentication",),
"DEFAULT_PERMISSION_CLASSES":("rest_framework.permissions.AllowAny",),
"DEFAULT_FILTER_BACKENDS":("django_filters.rest_framework.DjangoFilterBackend",
"rest_framework.filters.SearchFilter","rest_framework.filters.OrderingFilter"),
"DEFAULT_PAGINATION_CLASS":"mechanics.pagination.StandardPagination",
"DEFAULT_SCHEMA_CLASS":"drf_spectacular.openapi.AutoSchema",
}
SPECTACULAR_SETTINGS={"TITLE":"Mini Mechanic Service API","DESCRIPTION":"Mechanic service platform API","VERSION":"1.0.0","SERVE_INCLUDE_SCHEMA":False}
