from django.shortcuts import get_object_or_404, redirect, render
from .models import CartItem, Product, ShoppingCart
from .models import Rating
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
@login_required
def index(request):
    m= request.session.get('userid')
    products = Product.objects.all()
    products_with_ratings = []

    for product in products:
        average_rating = product.get_average_rating()
        products_with_ratings.append({'product': product, 'average_rating': average_rating})

    context = {'products_with_ratings': products_with_ratings,'m':m}
    return render(request, 'products/index.html', context)
@login_required
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
def add_to_cart(request, product_id):
    username = request.session.get('userid')
    user = get_object_or_404(User, username=username)

    product = get_object_or_404(Product, id=product_id)
    cart, created = ShoppingCart.objects.get_or_create(user=user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product,quantity=1)
    
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1  # تعيين كمية افتراضية عند إضافة عنصر جديد
    
    cart_item.save()

    return redirect('cart_view')

@login_required
def cart_view(request):
    username = request.session.get('userid')
    user = get_object_or_404(User, username=username)
    
    cart = ShoppingCart.objects.filter(user=user).first()
    cart_items = CartItem.objects.filter(cart=cart) if cart else []

    total_price = sum(item.product.price * item.quantity 
                      for item in cart_items)
    
    
    
    return render(request, 'products/CartItem.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def Remove(request,cartId):

    cart=CartItem.objects.filter(id=cartId)
    cart.delete()
    return redirect("cart_view")



@login_required
def SignOut(request):
    del request.session['userid']
    return redirect('singin')

