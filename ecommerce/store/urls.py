from django.urls import path
from . import views


urlpatterns = [
    path('', views.Store, name='Store'),
    path('', views.Main, name='Main'),    
    path('Cart/', views.Cart, name='Cart'),
    path('product/<int:pk>/', views.product_view, name="product_view"),
    path('Checkout/', views.Checkout, name='Checkout'),
    path('update_item/', views.updateItem, name='update_item') ,
    path('process_order/', views.ProcessOrder, name="process_order"),
] 
    