from django.db import models
from django.forms import ModelForm
from localflavor.us.models import USStateField
# from django.utils import timezone
from datetime import datetime, date

class UserManager(models.Manager):
    def basic_validator(self, postdata):
        errors = {}
        email_checker = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postdata['pw']) < 8:
            errors['pw'] = "Your password must be at least 8 characters"
        if len(postdata['fname']) < 2 or len(postdata['lname']) < 2:
            errors['name'] = "Your name must be at least 2 characters"
        if not email_checker.match(postdata['email']):
            errors['email'] = 'Email must be valid'
        if postdata['pw'] != postdata['confpw']:
            errors['pw'] = 'Password and Confirm Password do not match'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_pic = models.ImageField(
        upload_to='course_directory_path', 
        default= 'courses/blank-course.jpg',
        blank=True,
        null=True,
        )
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

class UserForm(ModelForm):
    class Meta:
        model = User
        fields =['first_name', 'last_name', 'profile_pic', 
        'email', 'password']

class Dish(models.Model):
    title = models.CharField(max_length=255)
    recipe = models.TextField
    description = models.TextField
    instructions = models.TextField
    ingredients = models.TextField
    prep = models.IntegerField
    cook = models.IntegerField
    servings = models.IntegerField
    profile_pic = models.ImageField(
        upload_to='course_directory_path', 
        default= 'dishes/blank-dish.jpg',
        blank=True,
        null=True,
        )
    poster = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')

class DishForm(ModelForm):
    class Meta:
        model = Dish
        fields = ['title', 'recipe', 'description', 'instructions',
        'ingredients', 'prep', 'cook', 'servings', 'profile_pic']

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, related_name='dish_comments', on_delete=models.CASCADE)

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'poster', 'dish']

class UserProfile(models.Model):
    profile_pic = models.ImageField(
        upload_to='course_directory_path', 
        default= 'users/blank-user.jpg',
        blank=True,
        null=True,
        )
    bio = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    birthday = models.DateField(blank=True, null=True)

class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'bio', 'location', 'birthday']

class Rating(models.Model):
    dish = models.ForeignKey(Dish, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    rating = models.IntegerField
    review = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['dish', 'user', 'rating', 'review']

class Category(models.Model):
# for grouping recipes into categories
    pass

class CategoryForm(ModelForm):
    pass
