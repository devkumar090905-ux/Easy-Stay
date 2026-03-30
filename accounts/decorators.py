from django.shortcuts import redirect
from functools import wraps
from django.contrib import messages

def landlord_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'landlord':
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'You do not have permission to access this page. Landlord access required.')
            return redirect('home')
    return wrap

def tenant_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'tenant':
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'You do not have permission to access this page. Tenant access required.')
            return redirect('home')
    return wrap
