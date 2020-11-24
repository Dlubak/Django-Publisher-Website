# signals module
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    :param sender: Class User.
    :param instance: The user instance.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


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
