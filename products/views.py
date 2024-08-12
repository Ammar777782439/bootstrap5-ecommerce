
from itertools import product
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
@login_required(redirect_field_name='account')
def index(request):
    # if not request.user.is_authenticated:#طريقه لتحقق من تسجيل الدخول للمستحدم
    #     return redirect('singin')
    

    m= request.user.id
    products = Product.objects.all()
    products_with_ratings = []
   
    for product in products:
        average_rating = product.get_average_rating()
        products_with_ratings.append({'product': product, 'average_rating': average_rating})

    context = {'products_with_ratings': products_with_ratings,'m':m}
    return render(request, 'products/index.html', context)


@login_required(redirect_field_name='account')
def detail(request, id):
    product = get_object_or_404(Product, id=id)
    ratings = product.ratings.all()  # الحصول على جميع التقييمات المرتبطة بالمنتج
    average_rating = product.get_average_rating()
    return render(request, 'products/product-item-detail.html', {
        'product': product,
        'ratings': ratings,
        'average_rating': average_rating,
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
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)
        
        cart_item.save()

        return redirect('cart_view')

@login_required

def cart_view(request):
    
    user = request.user.id
    cart_shop=ShoppingCart.objects.filter(user=user)
    cart_items=CartItem.objects.filter(cart__id__in=cart_shop)
    
    total_price=sum( itm.product.price*itm.quantity  for itm in cart_items)
    
    return render(request,'products/CartItem.html',{'cart_items':cart_items,'total_price':total_price})
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
    total_price=sum( itm.product.price*itm.quantity  for itm in cart_items)
    

    dostavka=request.GET.get('dostavka')
    print(dostavka)
    Shipping_Address=request.GET.get('Shipping_Address')
    
    
        # الحصول على الملف الشخصي للمستخدم باستخدام العلاقة المحددة في نموذج UserProfile
    user_profile = UserProfile.objects.get(user=user)
    
    return render(request, 'products/pageorder.html', {'user_profile': user_profile,'cart_items':cart_items,'total_price':total_price})







def pay(request):


    return render(request,'products/payment.html')







@login_required
def SignOut(request):
    
    logout(request)
    return redirect('singin')

