from django.db import models
from django.forms import ModelForm
from localflavor.us.models import USStateField
# from django.utils import timezone
from datetime import datetime, date

class Dish(models.Model):
    pass

class DishForm(ModelForm):
    pass

class Comment(models.Model):
    pass

class CommentForm(ModelForm):
    pass

class UserProfile(models.Model):
# everything about the user except name, email, password
    pass

class UserProfileForm(ModelForm):
    pass

class Rating(models.Model):
    pass

class RatingForm(ModelForm):
    pass

class Category(models.Model):
# for grouping recipes into categories
    pass

class CategoryForm(ModelForm):
    pass
