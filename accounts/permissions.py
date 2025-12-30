from django.shortcuts import redirect

def role_required(role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('tenant_login', slug=kwargs.get('slug'))
            if request.user.role != role:
                return redirect('tenant_login', slug=request.user.organisation.slug)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
