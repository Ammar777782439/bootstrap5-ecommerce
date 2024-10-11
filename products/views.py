
from itertools import product
from urllib import request
from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Sum, F
from accounts.models import UserProfile
from .models import CartItem, OrderItem, Product, ShoppingCart,Order
from .models import Rating
from django.conf import settings
from django.contrib.auth import authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def iameg(request):
    
    user=request.user.id
    profile=UserProfile.objects.get(user__id=user)

    return profile
    
@login_required(redirect_field_name='account')
def index(request):
    # if not request.user.is_authenticated:#طريقه لتحقق من تسجيل الدخول للمستحدم
    #     return redirect('singin')
    
    
    m= request.user.id
    products = Product.objects.all()
    products_with_ratings = []
   
    paginator = Paginator(products, 4) 
    page_number = request.GET.get('page')
    
    try:
        paginated_products = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)
    for product in paginated_products:
        average_rating = product.get_average_rating()
        products_with_ratings.append({'product': product, 'average_rating': average_rating})

    context = {'products_with_ratings': products_with_ratings,'m':m,'profile':iameg(request),'page_obj': paginated_products}
    return render(request, 'products/index.html', context)


@login_required(redirect_field_name='account')
def detail(request, id):
    product = get_object_or_404(Product, id=id)
    ratings = product.ratings.all()  # الحصول على جميع التقييمات المرتبطة بالمنتج
    average_rating = product.get_average_rating()
    return render(request, 'products/product-item-detail.html', {
        'product': product,
        'ratings': ratings,
        'average_rating': average_rating,'profile':iameg(request)
    })


@login_required
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        
        user = request.user
        product = get_object_or_404(Product, id=product_id)
        cart, created = ShoppingCart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product,quantity=quantity)
        
        if not created:
            # cart_item=CartItem.objects.filter(quantity=quantity,product=product)
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        
        cart_item.save()

        return redirect('cart_view')

@login_required


def cart_view(request):
 
    user = request.user.id
    
    
   
    cart_shop = ShoppingCart.objects.get(user=user)
    
        
    
    
    cart_items = CartItem.objects.filter(cart=cart_shop)
    
    
    cart_items = cart_items.annotate(total_price=F('product__price') * F('quantity')).order_by('total_price')
    
    
    total_price = cart_items.aggregate(total=Sum(F('product__price') * F('quantity')))['total'] or 0
    

    return render(request, 'products/CartItem.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'profile': iameg(request) 
    })
@login_required
def Remove(request,cartId):

    cart=get_object_or_404(CartItem, id=cartId)
    cart.delete()
    return redirect("cart_view")

@login_required

def add_to_comment(request):

    user=request.user
    pro_id=request.POST.get('product_id')
    pro=Product.objects.get(id=pro_id)
    score=request.POST.get('score')
    comment=request.POST.get('comment')
    data=Rating(user=user,product=pro,comment=comment,score=score)
    data.save()
    return redirect('product_detail',pro_id)


def addoeder(request):
    user = request.user
    cart = ShoppingCart.objects.filter(user=user).first()

    cart_items = CartItem.objects.filter(cart=cart)
    
    total_price = sum(itm.product.price * itm.quantity for itm in cart_items)

    dostavka = request.POST.get('dostavka')
    shipping_address = request.POST.get('Shipping_Address')

    # إنشاء الطلب
    order = Order.objects.create(
        user=user,
        total_price=total_price,
        shipping_address=shipping_address,
        shipping_method=dostavka,
        order_status='Pending'  # تعيين الحالة الافتراضية للطلب
    )

    # إضافة العناصر إلى الطلب
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    # حذف العناصر من السلة بعد إنشاء الطلب
    cart_items.delete()

    # الحصول على الملف الشخصي للمستخدم
    user_profile = UserProfile.objects.get(user=user)

    return redirect('order')
   
def order(request):

    user=request.user
    cart = ShoppingCart.objects.filter(user=user).first()
    cart_items = CartItem.objects.filter(cart=cart)

    total_price=cart_items.aggregate(total_price=Sum(F('product__price')*F('quantity'))) ['total_price']or 0


    # total_price=sum( itm.product.price*itm.quantity  for itm in cart_items)
    
    Shipping_Address=request.GET.get('Shipping_Address')
    
    
    user_profile = UserProfile.objects.get(user=user)
    
    return render(request, 'products/pageorder.html', {'user_profile': user_profile,'cart_items':cart_items,'total_price':total_price,'profile':iameg(request)})






@login_required
def SignOut(request):
    
    logout(request)
    return redirect('singin')



