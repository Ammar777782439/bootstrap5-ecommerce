from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('detail/<int:id>/',views.detail,name='product_detail'),
   path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('SignOut/', views.SignOut, name='SignOut'),
    path('Remove/<int:cartId>/', views.Remove, name='Remove'),
]

