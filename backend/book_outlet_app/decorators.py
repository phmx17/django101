from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs): # the wrapper replaces what the decorator is attached to
        if request.user.is_authenticated:
            return redirect('test')
        return view_func(request, *args, **kwargs) # this is the view itself
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs): # the wrapper replaces what the decorator is attached to
            group = None # must define in case no group is found
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs) # this is the view itself
            return redirect('not_authorized')
        return wrapper_func
    return decorator

