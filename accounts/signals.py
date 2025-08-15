from .models import User, UserProfile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print("Create the User Profile")
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print("User is updated")
        except:
            UserProfile.objects.create(user=instance)
            print("Profile didn't existed so created once")
@receiver(pre_save, sender=User)
def pre_save_create_profile_receiver(sender, instance, **kwargs):
    print(instance.username , " this user is being created ! ")