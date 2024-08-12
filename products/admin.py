from django.contrib import admin
from .models import Product
from .models import Category,Order,OrderItem,Rating
from .models import Rating,CartItem,ShoppingCart
admin.site.register(OrderItem)
admin.site.register(Rating)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(ShoppingCart)
# Register your models here.
