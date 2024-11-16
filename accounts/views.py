from typing import Counter
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from products.views import iameg
from products.models import Order, OrderItem, Product, Rating
from .models import UserProfile
from django.contrib.auth.decorators import login_required
import re #تحقق من الايميل 
from django.shortcuts import render, redirect
from django.db.models import Sum, F
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def signup(request):
    if request.method == 'POST':
        fname = request.POST.get('first', '')
        lname = request.POST.get('last', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        kay = request.POST.get('kay', '')
        phone = request.POST.get('Phone', '')
        password = request.POST.get('password', '')
        rpassword = request.POST.get('Rpassword', '')
        address = request.POST.get('Address', '')
        city = request.POST.get('city', '')
        house = request.POST.get('House', '')
        postal_code = request.POST.get('Postal_code', '')
        zip_code = request.POST.get('Zip', '')
        
        # التحقق من الحقول المطلوبة
        if not (name and email and password and rpassword):
            messages.error(request, 'يرجى ملء جميع الحقول المطلوبة.')
            return render(request, 'accounts/user-signup.html')

        # التحقق من اسم المستخدم والبريد الإلكتروني
        if User.objects.filter(username=name).exists():
            messages.error(request, 'اسم المستخدم موجود بالفعل')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'البريد الإلكتروني موجود بالفعل')
        else:
            if password == rpassword:
                user = User.objects.create_user(
                    first_name=fname, last_name=lname, username=name, email=email, password=password
                )
                user.save()
                # إضافة UserProfile
                userprofile = UserProfile(
                    user=user, phone=phone, kayphone=kay, address=address, city=city,
                    postal_code=postal_code, zip_code=zip_code
                )
                userprofile.save()
                messages.success(request, "تم إنشاء المستخدم بنجاح")
                return redirect('singin')  
            else:
                messages.error(request, 'كلمتا المرور غير متطابقتين')
    
    return render(request, 'accounts/user-signup.html')

def signin(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        password = request.POST.get("password")
        
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة')
    
    return render(request, 'accounts/user-signin.html')

def profile(request):

    
    # order_item=[ user_id.product for user_id in  OrderItem.objects.filter(order__id=order[0])]
    # counter=Counter(order)
    # s=sum(counter.values()) 
    # order_item=OrderItem.objects.annotate(total=F('product'))
    if request.user.is_authenticated:
     user_id=request.user.id
     profile=UserProfile.objects.get(user__id=user_id)

     order_count=[ user_id.id for user_id in  Order.objects.filter(user=user_id)]
     counter=Counter(order_count)
     s=sum(counter.values()) 

    
     order=Order.objects.filter(user__id=user_id)
    
     order_item=OrderItem.objects.filter(order__id__in=order)
    
    
    


     paginator=Paginator(order,5)
     page_number=request.GET.get('page')
     
     try:
        paginator_order=paginator.page(page_number)
     except PageNotAnInteger:
        paginator_order=paginator.page(1)
     except EmptyPage:
        paginator_order=paginator.page(paginator.num_pages)


    

     print(order)
    

     return render(request,'accounts/profile.html',{'profile':iameg(request),'order_item':order_item,'orders':order,'paginator_order':paginator_order,'order_count':s})
    else:
         return render(request, 'accounts/user-signin.html')
def delete(request,id):
    
    cart=get_object_or_404(Order, id=id)
    cart.delete()
    return redirect("profile")

def delete_comment(request,id):
    
    cart=get_object_or_404(Rating, id=id)
    cart.delete()
    return redirect("view_to_comment")


def view_to_comment(request):
     
    user=request.user.id
    pro=Rating.objects.filter(user=user)
    print(pro)
    return render(request,'accounts/comment.html',{'profile':iameg(request),'pro':pro})
    


    
def view_to_comment_test(request):
    user_id=request.user.id

    order=[ user_id.id for user_id in  Order.objects.filter(user=user_id)]
    
    product_namee=[ user_id.product for user_id in  OrderItem.objects.filter(order__id=order[0])]
    counter=Counter(order)
    s=sum(counter.values()) 
    print(product_namee)
    return render(request,'accounts/comment _copy.html',{'product_namee':s})
    