from django.urls import path
from . import views

urlpatterns = [
    path('landlord/signup/', views.landlord_signup_view, name='landlord_signup'),
    path('tenant/signup/', views.tenant_signup_view, name='tenant_signup'),
    path('landlord/login/', views.landlord_login_view, name='landlord_login'),
    path('tenant/login/', views.tenant_login_view, name='tenant_login'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('logout/', views.logout_view, name='logout'),
]
