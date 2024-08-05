from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.decorators import login_required
import re #تحقق من الايميل 

def signup(request):
    fname = request.POST.get('first', '')
    lname = request.POST.get('last', '')
    name = request.POST.get('name', '')
    Email = request.POST.get('email', '')
    kay = request.POST.get('kay', '')
    phon = request.POST.get('Phone', '')
    password = request.POST.get('password', '')
    Rpassword = request.POST.get('Rpassword', '')
    check = request.POST.get('check', False)
    
    
    if not (name and Email and password and Rpassword):
        messages.error(request, 'يرجى ملء جميع الحقول المطلوبة.')
        return render(request, 'accounts/user-signup.html')
    
    if User.objects.filter(username=name).exists():
        messages.error(request, 'اسم المستخدم موجود بالفعل')
    elif User.objects.filter(email=Email).exists():
        messages.error(request, 'البريد الإلكتروني موجود بالفعل')
    else:
        if password == Rpassword:
            user = User.objects.create_user(
                first_name=fname, last_name=lname, username=name, email=Email, password=password
            )
            user.save()
            # إضافة UserProfile
            userprofile = UserProfile(user=user, phone=phon, kayphone=kay)
            userprofile.save()
            messages.success(request, "تم إنشاء المستخدم بنجاح")
            return redirect('singin')  
        else:
            messages.error(request, 'كلمتا المرور غير متطابقتين')
    
    return render(request, 'accounts/user-signup.html',{'userprofile':userprofile})

def signin(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(username=name)
            
            if user.check_password(password):
                request.session['userid'] = user.username
                return redirect('index')
        except User.DoesNotExist:
            pass
    
    return render(request, 'accounts/user-signin.html')

    