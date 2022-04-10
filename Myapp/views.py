from django.shortcuts import render, redirect, get_object_or_404,reverse
from .forms import UserRegistration, UserLoginForm, UpdateProfileForm, UpdateUserInfoForm, AddBlogForm, UpdateBlogForm,AddCommmentForm, NewPasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Blog,Profile
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user



#get author from model
def get_author(user):
    qs = Profile.objects.filter(author = user)
    if qs.exists():
        for q in qs:
            print(q.author)
            return q.author
    return None 


def like_Fun(request,id):
    user = request.user 
    blog = get_object_or_404(Blog, id = request.POST.get('blog_id'))
    is_liked = False
    if user in blog.likes.all():
        blog.likes.remove(user)
        is_liked = False
    else:
        blog.likes.add(user) 
        is_liked = True   
    return redirect(reverse('blogdetails', args = [str(id)]))
    #that's how u get redirect to certain url with id,but dont need this here


    
    

# Create your views here.
def index(request): 
     #request.user won't work as filter in profile because user is not logged in.to avoid it user login required
    blog = Blog.objects.all().order_by('-date')
           
    context = {
        'blog':blog,

    }
    return render(request, 'Myapp/index.html', context)


def blog_details(request, id): 
    blog = get_object_or_404(Blog, id = id)
    is_liked = False
    if blog.likes.filter(id = request.user.id).exists():
        is_liked = True
    if request.method == 'POST':     
        fm = AddCommmentForm(request.POST)
        if fm.is_valid():
            fm.instance.author = request.user
            fm.instance.blog = blog
            fm.save()
            return redirect(reverse('blogdetails' ,args = [str(id)])) 
    else:
        fm = AddCommmentForm()           
           
    context = {
        'blog':blog,
        'is_liked':is_liked,
        'total_likes':blog.total_likes,
        'form':fm,

    }
    print(is_liked)
    return render(request, 'Myapp/blogdetail.html', context)


def about(request):
    return render(request, 'Myapp/about.html')


@unauthenticated_user
def sign_up(request):
    if request.method == 'POST':
        fm = UserRegistration(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request, "You have registerd,Successfully! ")

    else:
        fm = UserRegistration()        

    return render(request, 'Myapp/signup.html', {'form':fm})

#login view
@unauthenticated_user
def sign_in(request):
    if request.method =='POST':
        fm = UserLoginForm(request = request, data = request.POST)
        if fm.is_valid():
            username = fm.cleaned_data.get('username')
            password = fm.cleaned_data.get('password')
            
            user = authenticate(
                username = username,
                password = password
            )
            print(user)
            if user is not None:
                login(request, user)
                return redirect('homepage') 
            else:
                messages.warning(request,"username or password is incorrect")    
    else:
        fm = UserLoginForm()             
    context ={
        'form':fm
    }
    return render(request,'Myapp/signin.html',context)

@login_required(login_url = 'loginpage')
def dashbord(request):
    user= request.user
    profile = Profile.objects.filter(author = user)
    blog = Blog.objects.filter(author = user).order_by('-date')
    f1 = Blog.objects.filter(author = user).order_by('-date').first()
    context ={
        'blog':blog,
        'profile':profile,
        'lastpost':f1
        
    }
    return  render(request,'Myapp/dashbord.html', context)   

login_required(login_url = 'loginpage')
def sign_out(request):
    logout(request)
    return redirect('homepage')    
     


def update_Info(request):
    if request.method =='POST':
        p_form = UpdateProfileForm(
                                request.POST,
                                request.FILES,
                                instance = request.user.profile
                                )
        u_form = UpdateUserInfoForm(
                                request.POST,
                                instance = request.user
                                )
        if u_form.is_valid and p_form.is_valid():
            if not p_form.instance.image:
                p_form.instance.image = 'default.png'        
            u_form.save()
            p_form.save()
            messages.success(request,'Your Profile has been Updated Successfully!')
            return redirect('profile')
            

    else:
        p_form = UpdateProfileForm(

                                instance = request.user.profile

                                )
        u_form = UpdateUserInfoForm(
                                instance = request.user
                                )  

    user= request.user
    profile = Profile.objects.filter(author = user)
    blog = Blog.objects.filter(author = user)
    f1 = Blog.objects.filter(author = user).order_by('-date').first()
    print(p_form)
          
    context = {
        'blog':blog,
        'profile':profile,
        'lastpost':f1,
        'p_form':p_form,
        'u_form':u_form
    }
    return render(request,'Myapp/updateinfo.html', context)

@login_required(login_url ='loginpage')
def add_blog(request):
    if request.method == 'POST':
        fm = AddBlogForm(request.POST)
        author = get_author(request.user)
        if fm.is_valid():
            fm.instance.author = author #i can directly put request.user but i don't know why i m dong this
            fm.save()
            messages.success(request,"Blog Posted Successfully!")
            fm = AddBlogForm()
    else:
        fm = AddBlogForm()


    context ={
        'form':fm
    }
    return render(request, 'Myapp/addblog.html',context)


def update_blog(request, id):
    if request.method =='POST':
        pi = get_object_or_404(Blog, pk = id)
        fm = UpdateBlogForm(request.POST, instance = pi)
        if fm.is_valid():
            fm.save()
            messages.success(request,"Blog Post Updated Successfully!")    
    else:
        pi = get_object_or_404(Blog, pk = id)
        fm = UpdateBlogForm(instance = pi)

    context ={
        'form':fm,
        'blog':pi
    }   
    print(pi.author.id)
    print(request.user.id)
    return render(request, 'Myapp/updateblog.html',context)    


def delete_blog(request, id):
    if request.method == 'POST':
        ps = Blog.objects.filter(pk =id)
        ps.delete()
        messages.success(request, "Blog post deleted,successfully!")
        return redirect('profile')
        

    else:
        ps = Blog.objects.filter(pk = id)
        print(ps)
    context ={
        'blog':ps
    }        
    return render(request, 'Myapp/deleteblog.html',context)


def New_Pass(request):
    fm = NewPasswordForm('request.user')
    content = {
        'form':fm
    }
    return render(request, 'Myapp/newpass.html',content)


