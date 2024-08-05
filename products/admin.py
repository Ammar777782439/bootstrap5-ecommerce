from django.contrib import admin
from .models import Product
from .models import Category
from .models import Rating,CartItem,ShoppingCart


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(ShoppingCart)
# Register your models here.
