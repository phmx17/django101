from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs): # the wrapper replaces what the decorator is attached to
        if request.user.is_authenticated:
            return redirect('test')
        return view_func(request, *args, **kwargs) # this is the view itself
    return wrapper_func