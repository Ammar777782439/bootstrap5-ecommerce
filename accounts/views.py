from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.decorators import login_required
import re #تحقق من الايميل 
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile

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
        
        try:
            user=authenticate(request,username=name,password=password)
            if user is not None:
                login(request, user)
                
                request.session['userid'] = user.username
                return redirect('index')
        except User.DoesNotExist:
            pass
    
    return render(request, 'accounts/user-signin.html')

    