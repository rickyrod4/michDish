from django.db.models.signals import post_save
# from .models import UserProfile
# from login_app.models import User
# from django.dispatch import receiver

# @receiver(post_save, sender=User)
# def create_user_profile(sender, **kwargs):
#     user = kwargs["instance"]
#     if kwargs["created"]:
#         profile = UserProfile(user=user)
#         if hasattr(user, 'birth_date'):
#             profile.birth_date = user.birth_date
#         profile.save()