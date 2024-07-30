from django.contrib import admin
from .models import Product
from .models import Category
from .models import Rating


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Rating)
# Register your models here.
