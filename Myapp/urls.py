from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('signup/', views.sign_up ,name ='signuppage'),
    path('signin/', views.sign_in ,name ='loginpage'),
    path('about/', views.about ,name ='aboutpage'),
    path('profile/', views.dashbord ,name ='profile'),
    path('addblog/', views.add_blog ,name ='addblogpage'),
    path('updateblog/<int:id>', views.update_blog ,name ='updateblogpage'),
    path('deleteblog/<int:id>', views.delete_blog ,name ='deleteblogpage'),
    path('logout/', views.sign_out ,name ='logoutpage'),
    path('profile/update/', views.update_Info, name ='updateinfopage'),
    path('likes/<int:id>', views.like_Fun ,name ='like_post'),
    path('blogdetails/<int:id>', views.blog_details ,name ='blogdetails'),
    path('password-reset',
     auth_views.PasswordResetView.as_view(template_name = 'MYapp/passwordreset.html') ,name ='password_reset'),
    path('password-reset-done', 
    auth_views.PasswordResetDoneView.as_view(template_name = 'Myapp/passwordresetdone.html') ,name ='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name ='Myapp/passwordresetconfirm.html') ,name ='password_reset_confirm'),
    path('password-reset-complete',
     auth_views.PasswordResetCompleteView.as_view(template_name ='Myapp/passwordresetcomplete.html') ,name ='password_reset_complete'),
]
