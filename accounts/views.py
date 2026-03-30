from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
User = get_user_model()
from django.core.mail import send_mail
from django.conf import settings
import random
from .models import OTP
from .forms import SignupForm, LoginForm, OTPForm

def signup_view_base(request, role):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Email already registered')
                return render(request, f'{role}_signup.html', {'form': form})
            
            otp_code = str(random.randint(100000, 999999))
            OTP.objects.create(email=email, otp=otp_code)
            
            send_mail(
                'EasyStay Registration - Your OTP',
                f'Welcome to EasyStay! Your verification code is: {otp_code}',
                settings.EMAIL_HOST_USER,
                [email]
            )
            
            request.session['signup_data'] = {
                'username': form.cleaned_data.get('username'),
                'email': email,
                'password': form.cleaned_data.get('password'),
                'role': role,
            }
            return redirect('verify_otp')
    else:
        form = SignupForm(initial={'role': role})
    return render(request, f'{role}_signup.html', {'form': form})

def landlord_signup_view(request):
    return signup_view_base(request, 'landlord')

def tenant_signup_view(request):
    return signup_view_base(request, 'tenant')

def verify_otp_view(request):
    signup_data = request.session.get('signup_data')
    if not signup_data:
        return redirect('home')

    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_entered = form.cleaned_data.get('otp')
            email = signup_data.get('email')
            otp_obj = OTP.objects.filter(email=email, otp=otp_entered).last()
            
            if otp_obj and otp_obj.is_valid():
                user = User.objects.create_user(
                    username=signup_data['username'],
                    email=signup_data['email'],
                    password=signup_data['password'],
                    role=signup_data['role']
                )
                
                send_mail(
                    'EasyStay - Registration Successful',
                    f'Hi {user.username},\n\nYour account has been created successfully as a {signup_data["role"]}.\n\nThank you for joining EasyStay!',
                    settings.EMAIL_HOST_USER,
                    [user.email]
                )
                
                login(request, user)
                del request.session['signup_data']
                otp_obj.delete()
                return redirect('home')
            else:
                form.add_error('otp', 'Invalid or expired OTP')
    else:
        form = OTPForm()
    return render(request, 'verify_otp.html', {'form': form})

def login_view_base(request, role):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                if user.role == role:
                    login(request, user)
                    return redirect('home')
                else:
                    form.add_error(None, f'No {role} account found with these credentials.')
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, f'{role}_login.html', {'form': form, 'role': role})

def landlord_login_view(request):
    return login_view_base(request, 'landlord')

def tenant_login_view(request):
    return login_view_base(request, 'tenant')

def logout_view(request):
    logout(request)
    return redirect('home')
