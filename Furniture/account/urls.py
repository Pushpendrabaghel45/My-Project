# from django.urls import path
# from . import views

# urlpatterns = [
#     path('dashboard/', views.admin_dashboard, name='dashboard'),
# ]
from django.urls import path
from account.views import admin_dashboard
from account import views

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'), 
    path('dashboard/products/', views.admin_products, name='admin_products'),
    path('dashboard/logout/', views.admin_logout, name='logout'),

    path('product/add/', views.add_product, name='add_product'),
    path('product/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:id>/', views.delete_product, name='delete_product'), 

    path('dashboard/categories/', views.admin_categories, name='admin_categories'),
    path('dashboard/admin_personal_details/', views.admin_personal_details, name='admin_personal_details'),
    path('dashboard/categories/add/', views.admin_category_add, name='admin_category_add'),
    path('dashboard/categories/edit/<int:id>/', views.admin_category_edit, name='admin_category_edit'),
    path('dashboard/categories/delete/<int:id>/', views.admin_category_delete, name='admin_category_delete'),
 
]

   