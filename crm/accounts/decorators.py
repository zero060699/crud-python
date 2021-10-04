from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wraper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wraper_func

def allowed_users(allowed_roles=[]):
    def decorators(view_func):
        def wraper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorize')
        return wraper_func
    return decorators

def admin_only(view_func):
    def wraper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':
            return redirect('user-page')
        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wraper_func