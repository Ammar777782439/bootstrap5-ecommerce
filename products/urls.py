from django.urls import path
from . import views

urlpatterns = [
    path('Remove/<int:cartId>/', views.Remove, name='Remove'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    
    
   
    path('detail/<int:id>/',views.detail,name='product_detail'),
    
   path('',views.index,name='index'),
    path('cart/', views.cart_view, name='cart_view'),
    path('SignOut/', views.SignOut, name='SignOut'),
    path('order/', views.order, name='order'),
     path('orderR/', views.addoeder, name='addorder'),
      path('comment/', views.add_to_comment, name='add_to_comment'),
     
    
]

