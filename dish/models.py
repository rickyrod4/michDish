from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
#from localflavor.us.models import USStateField
# from django.utils import timezone
from datetime import datetime, date
from django.db.models import Avg
import math

class Category(models.Model):
    name = models.CharField(max_length=20)
    profile_pic = models.ImageField(
        upload_to='categories/', 
        default= 'categories/blank-category.jpg',
        blank=True,
        null=True,
        )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    def __str__(self):
        return self.name

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'profile_pic']
        widgets = {
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control-file',}),
            'name' : forms.TextInput(attrs={'class':'form-control'}),
       }        

def dish_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/dish_<id>/<filename>
    return 'dish_{0}/{1}'.format(instance.id, filename)

class Dish(models.Model):
    title = models.CharField(max_length=255)
    recipe = models.TextField(help_text="Instructions for how to make the dish.")
    description = models.TextField(blank=True, help_text="Describe the dish, its history and why you were inspired to make it.")
    ingredients = models.TextField(help_text="Add each ingredient on a new line.")
    prep_time = models.IntegerField(help_text="Prep time in minutes.")
    cook_time = models.IntegerField(help_text="Cook time in minutes.")
    servings = models.IntegerField()
    profile_pic = models.ImageField(
        upload_to=dish_directory_path, 
        default= 'dishes/blank-dish.jpg',
        blank=True,
        null=True,
        )
    categories = models.ManyToManyField(Category, related_name='dishes', help_text="Select all categories that apply.")
    poster = models.ForeignKey(User, related_name='user_dishes', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_dishes')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    def get_average_rating(self):
        average = self.ratings.aggregate(Avg('rating'))['rating__avg'] or 0
        return math.ceil(average)
        #return Rating.objects.filter(dish=dish).aggregate(Avg('rating'))['rating__avg'] or 0

class DishForm(ModelForm):
    class Meta:
        model = Dish
        fields = ['title', 'description', 'ingredients', 'recipe', 
        'prep_time', 'cook_time', 'servings', 'profile_pic', 'categories']
        widgets = {
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control-file',}),
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control'}),
            'recipe': forms.Textarea(attrs={'class': 'form-control'}),
            'prep_time' : forms.TextInput(attrs={'class':'form-control'}),
            'cook_time' : forms.TextInput(attrs={'class':'form-control'}),
            'servings' : forms.TextInput(attrs={'class':'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
       }


class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, related_name='dish_comments', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        # pylint: disable=E1101
        return f'{self.poster.first_name} {self.poster.last_name[0]} comment on {self.dish.title}'

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.id, filename)
class UserProfile(models.Model):
    profile_pic = models.ImageField(
        upload_to= user_directory_path, 
        default= 'users/blank-user.jpg',
        blank=True,
        null=True,
        )
    bio = models.TextField(blank=True, help_text="Tell us about yourself, chef!")
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    birthday = models.DateField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        # pylint: disable=E1101
        return f'{self.user.get_full_name()} Profile'

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'birthday', 'profile_pic']
        widgets = {
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control-file',}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'location' : forms.TextInput(attrs={'class':'form-control'}),
            'birth_date': forms.DateTimeInput(attrs={'class': 'form-control'}),
       }


def rating_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/dish_<id>/<filename>
    return 'dish_{0}/{1}'.format(instance.dish.id, filename)

class Rating(models.Model):
    dish = models.ForeignKey(Dish, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.TextField()
    profile_pic = models.ImageField(
        upload_to=dish_directory_path, 
        blank=True,
        null=True,
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        # pylint: disable=E1101
        return f'{self.user.first_name} {self.user.last_name[0]} rated {self.dish.title} {self.rating} stars' 

class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'review', 'profile_pic']