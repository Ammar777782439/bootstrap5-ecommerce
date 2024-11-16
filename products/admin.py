from django.contrib import admin
from django.http import HttpRequest
from .models import Product
from .models import Category,Order,OrderItem,Rating
from .models import Rating,CartItem,ShoppingCart
admin.site.register(OrderItem)
admin.site.register(Rating)
admin.site.register(Order)

admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(ShoppingCart)


class redonlayadmain:
    def has_add_permission(self, request, obj=None):
        return False
    def has_view_permission(self, request,obj=None ):
        return True
    
    def has_delete_permission(self, request,obj=None ):
        return False
    def has_change_permission(self, request,obj=None ):

        # if request.user.has_perm('product.change_product'):
        #     return False
        # else:
           return True
@admin.register(Product)
class ProductAdmain(redonlayadmain,admin.ModelAdmin):

    list_display=('name',)

    def get_form(self,request,obj=None,**kwargs):
        form=super().get_form(request,obj,**kwargs)
        is_superuser=request.user.is_superuser

        if not is_superuser:
            form.base_fields['name'].disabled=True
        return form
    