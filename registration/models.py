from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save


def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/' + filename

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #OneToOneFiel refiere a que 1 solo puede tener 1 perfil
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['user__username']

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
        #print("Se acaba de crear un usuario y su perfil enlazado")

# old_avatar = ""

# @receiver(pre_save, sender=Profile)
# def signal(sender, instance, update_fields=None, **kwargs):
#     old_instance = Profile.objects.get(id=instance.id)
#     global old_avatar
#     old_avatar = old_instance.avatar

# @receiver(post_save, sender=Profile)
# def delete_avatar(sender, instance, **kwargs):
#         miProfile = Profile.objects.get(pk=instance.pk)
#         nuevo_avatar = miProfile.avatar

#         if old_avatar != "" and nuevo_avatar == "":
#             old_avatar.delete()