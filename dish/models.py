from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
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


#class User(models.Model):
    #first_name = models.CharField(max_length=50)
    #last_name = models.CharField(max_length=50)
    #email = models.CharField(max_length=50)
    #password = models.CharField(max_length=50)
    #created_at = models.DateField(auto_now_add=True)
    #updated_at = models.DateField(auto_now=True)
    #objects = UserManager()

class UserForm(ModelForm):
    class Meta:
        model = User
        fields =['first_name', 'last_name', 'profile_pic', 
        'email', 'password']

class Category(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    def __str__(self):
        return self.name

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']

def dish_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'dish_{0}/{1}'.format(instance.id, filename)
class Dish(models.Model):
    title = models.CharField(max_length=255)
    recipe = models.TextField()
    description = models.TextField(blank=True)
    ingredients = models.TextField()
    prep_time = models.IntegerField()
    cook_time = models.IntegerField()
    servings = models.IntegerField()
    profile_pic = models.ImageField(
        upload_to='course_directory_path', 
        default= 'dishes/blank-dish.jpg',
        blank=True,
        null=True,
        )
    categories = models.ManyToManyField(Category, related_name='dishes')
    poster = models.ForeignKey(User, related_name='user_dishes', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_dishes')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class DishForm(ModelForm):
    class Meta:
        model = Dish
        fields = ['title', 'recipe', 'description',
        'ingredients', 'prep_time', 'cook_time', 'servings', 'profile_pic', 'categories']


def comment_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'comment_{0}/{1}'.format(instance.id, filename)
class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, related_name='dish_comments', on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='course_directory_path', 
        default= 'dishes/blank-dish.jpg',
        blank=True,
        null=True,
        )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        # pylint: disable=E1101
        return f'{self.poster.first_name} {self.poster.last_name[0]} comment on {self.dish.title}'

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'poster', 'dish']

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.id, filename)
class UserProfile(models.Model):
    profile_pic = models.ImageField(
        upload_to='user_directory_path', 
        default= 'users/blank-user.jpg',
        blank=True,
        null=True,
        )
    bio = models.TextField(blank=True)
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
        fields = ['profile_pic', 'bio', 'location', 'birthday']

class Rating(models.Model):
    dish = models.ForeignKey(Dish, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        # pylint: disable=E1101
        return f'{self.user.first_name} {self.user.last_name[0]} rated {self.dish.title} {self.rating} stars' 

class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['dish', 'user', 'rating', 'review']