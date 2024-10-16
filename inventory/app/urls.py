from django.urls import path
from .views.category import get_create_category,get_update_delete_category,category_matrics
from .views.products import get_create_products,get_update_delete_product,product_matrics
from .views.supplier import get_create_supplier,get_update_delete_supplier,supplier_matrics
from .views.auth import create_user,login_view,logout_view

urlpatterns = [
    path('user/signup', create_user),
    path('user/login', login_view),
    path('user/logout', logout_view),
    
    
    path('categories/', get_create_category),
    path('categories/<id>', get_update_delete_category),
    path('category/matrics', category_matrics),
    
    path('products/', get_create_products),
    path('products/<id>', get_update_delete_product),
    path('product/matrics', product_matrics),
    
    path('suppliers/', get_create_supplier),
    path('suppliers/<id>', get_update_delete_supplier),
    path('supplier/matrics', supplier_matrics),
    
]