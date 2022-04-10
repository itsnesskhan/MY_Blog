from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Categroy(models.Model):
    name = models.CharField(max_length = 50) #if  you said field null true, meas there alreay user withourt thait feidld

    def __str__(self):
        return self.name

class Blog(models.Model):
    author = models.ForeignKey(User,on_delete = models.CASCADE )
    title = models.CharField(max_length =100)
    desc  = models.TextField()
    date  = models.DateTimeField(auto_now_add = True)
    categroy = models.ForeignKey(Categroy,related_name ='blogs', on_delete =models.SET_NULL, null =True)
    likes = models.ManyToManyField(User, related_name ='likes', default = None, blank = True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()  

    def get_comments(self):
        return self.commments.all().order_by('-created')    
      

class Profile(models.Model):
    author = models.OneToOneField(User, on_delete = models.CASCADE, related_name='profile')
    image = models.ImageField( default ='default.png', upload_to = 'images', blank = True)
    city  = models.CharField(max_length = 100, blank= True)

    def __str__(self):
        return str(self.author)


    def save(self, *args, **kwargs): 
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.mode in ("RGBA", "P"):
            img.convert("RGB")
        if img.height> 300 or img.width >300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


    


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add =True)
    updated = models.DateTimeField(auto_now = True)
    blog = models.ForeignKey(Blog, related_name = 'comments', on_delete = models.CASCADE)
    content = models.TextField(blank = True )


    def __str__(self):
        return 'comment on {} by {}'.format(self.blog ,self.author)
