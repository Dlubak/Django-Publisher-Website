from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.CharField(max_length=100, default='')

# def create_user_profile(sender, instance, created, **kwargs):
#     """
#     :param sender: Class User.
#     :param instance: The user instance.
#     """
#     if created:
#         # Seems the following also works:
#         #   UserProfile.objects.create(user=instance)
#         # TODO: Which is correct or better?
#         profile = UserProfile(user=instance)
#         profile.save()

# post_save.connect(create_user_profile,
#                   sender=User,
#                   dispatch_uid="users-profilecreation-signal")
# #post_save.conntext(create_profile, sender=User)