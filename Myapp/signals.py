from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Blog
@receiver(post_save,sender = User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(author = instance)
        print("get called")


@receiver(post_save,sender = User)
def save_profile(sender,instance,created, **kwargs):
    print("profile has been created")
    instance.profile.save()

