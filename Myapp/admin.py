from django.contrib import admin
from .models import Blog,Profile,Categroy,Comment

# Register your models here.
@admin.register(Categroy)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Blog)
class UserAdmin(admin.ModelAdmin):
    list_display = ['title', 'desc','date','categroy', 'author']

@admin.register(Profile)
class UserAdmin(admin.ModelAdmin):
    list_display = ['author','image','city']    

admin.site.register(Comment)       
