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
        check = request.POST.get('check', False)
        
        # التحقق من الحقول المطلوبة
        if not (name and email and password and rpassword):
            messages.error(request, 'يرجى ملء جميع الحقول المطلوبة.')
            return render(request, 'accounts/user-signup.html')
        
        else:
          if password == rpassword:
             user = User.objects.create_user(
                    first_name=fname, last_name=lname, username=name, email=email, password=password
                )
          userprofile,created=UserProfile.objects.get_or_create(
                   user=user, phone=phone, kayphone=kay, address=address, city=city,
                    postal_code=postal_code, zip_code=zip_code)
          userprofile.save()
          
         
                
               
        # # التحقق من اسم المستخدم والبريد الإلكتروني
        # if User.objects.filter(username=name).exists():
        #     messages.error(request, 'اسم المستخدم موجود بالفعل')
        # elif User.objects.filter(email=email).exists():
        #     messages.error(request, 'البريد الإلكتروني موجود بالفعل')
        # else:
        #     if password == rpassword:
        #         user = User.objects.create_user(
        #             first_name=fname, last_name=lname, username=name, email=email, password=password
        #         )
        #         user.save()
        #         # إضافة UserProfile
        #         userprofile = UserProfile(
        #             user=user, phone=phone, kayphone=kay, address=address, city=city,
        #             postal_code=postal_code, zip_code=zip_code
        #         )
        #         userprofile.save()
        #         messages.success(request, "تم إنشاء المستخدم بنجاح")
        #         return redirect('singin')  
        #     else:
        #         messages.error(request, 'كلمتا المرور غير متطابقتين')
    
    return render(request, 'accounts/user-signup.html')

def signin(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        password = request.POST.get("password")
        
        try:
            user=authenticate(request,username=name,password=password)
            if user is not None:
                login(request, user)
                
                request.session['userid'] = user.username
                return redirect('index')
        except User.DoesNotExist:
            pass
    
    return render(request, 'accounts/user-signin.html')


def profile(request):
    user=request.user.id
    profile=UserProfile.objects.get(user__id=user)
    
    order=Order.objects.filter(user__id=user)

    order_item=OrderItem.objects.filter(order__id__in=order)
    # order_item=OrderItem.objects.annotate(total=F('product'))
    
    


    paginator=Paginator(order,5)
    page_number=request.GET.get('page')
     
    try:
        paginator_order=paginator.page(page_number)
    except PageNotAnInteger:
        paginator_order=paginator.page(1)
    except EmptyPage:
        paginator_order=paginator.page(paginator.num_pages)


    

    print(order)
    

    return render(request,'accounts/profile.html',{'profile':iameg(request),'order_item':order_item,'orders':order,'paginator_order':paginator_order})

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
    