from django import forms
from django.contrib.auth.models import User
from .models import Blog,Profile, Comment
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UsernameField, SetPasswordForm


class UserRegistration(UserCreationForm):
    username = forms.CharField(
        label_suffix ="-",
        widget = forms.TextInput(attrs ={'placeholder':'Username'})
        )
    password1 = forms.CharField(
        label_suffix ="-",
        label ="Password" ,
        widget = forms.PasswordInput(attrs ={'placeholder':'Password'})
        )
    password2 = forms.CharField(
        label_suffix ="-",
        label ="Confirm Passowrd" ,
        widget = forms.PasswordInput(attrs ={'placeholder':'Confirm Password'}) 
        )
    first_name = forms.CharField(
        label_suffix ="*",
        label ="First Name" ,
        widget = forms.TextInput(attrs ={'placeholder':'First Name'})
        )
    last_name = forms.CharField(
        label_suffix ="*",
        label ="Last Name" ,
        widget = forms.TextInput(attrs ={'placeholder':'Last Name'})
        )

    class Meta:
        model = User
        
        fields = ('username','first_name','last_name','password1','password2')


class UserLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "username or password you enter is incorrect!"
            
        ),
        'inactive': _("This account is inactive."),
    }
    username = UsernameField(label_suffix =":",
                widget=forms.TextInput(attrs={'autofocus': True,'placeholder':'Username'}))
    password = forms.CharField(label_suffix =":",
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password','placeholder':'Password'}),
    )

    class Meta:
        model = User
        fields= '__all__'



class UpdateUserInfoForm(forms.ModelForm):
    
    class Meta:
        model = User
        
        fields = ('username','first_name','last_name')
    
class UpdateProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('image','city')

class AddBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields= ['title','desc','categroy']   

class UpdateBlogForm(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = ['title','desc','categroy']


class AddCommmentForm(forms.ModelForm):#label suffix change in form control calss not work in crispy form
    content = forms.CharField(label_suffix =" ", label ="", widget = forms.Textarea(attrs = {'class':'form-control','placeholder':'Add a comment...', 'rows':3,'cols':5}))
    class Meta:
        model = Comment
        fields = ['content']

class NewPasswordForm(SetPasswordForm):

    class Meta:
        model = User
        fields = '__all__'
        labels = {'new_password2':'Confirm Password'}

