from django.shortcuts import redirect

def unauthenticated_user(view_fun):
    def wrapper_fun(request, *args, **kwargs):
        print("its working")
        if request.user.is_authenticated:
            return redirect('homepage')

        return view_fun(request,*args,**kwargs)
    return wrapper_fun    
