from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
# from login_app.models import User
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from django.contrib import messages
from django.db.models import Avg, F, Q
from django.core.paginator import Paginator
import math

DISHES_PER_PAGE = 6


# Create your views here.
def index(request):
    dishes = Dish.objects.all() #.order_by('date')

    # paginator = Paginator(dishes, DISHES_PER_PAGE) # NUMBER OF dishes per page TO DISPLAY
    # page_number = request.GET.get('page') or 1
    # page_obj = paginator.get_page(page_number)

    context = {
        'foo': 'bar',
        'user': request.user,
        'dishes': dishes,
    #     'page_obj': page_obj,
    #     'current_page': page_number,
    }
    return render(request, 'dish/dashboard.html', context)

@login_required(login_url='/accounts/login/')
def get_dish(request):
    # New Dish Form

    user = request.user #User.objects.get(id=request.session['user_id'])
    dish = Dish(poster=user) #create a new Dish object with the current user as the creator

    #POST request ==> save new course
    if request.method == 'POST':
        
        # populate the form with the form's POST data, the form's FILES dictionary
        # and the Dish instance we created above 
        form = DishForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():
        
            # save the form, but do not commit changes to the database yet
            # we need to do some extra work for the picture
            dish = form.save(commit=False)
        
            # if the user deleted the previous photo, add the default photo
            if form.cleaned_data['profile_pic'] == None or form.cleaned_data['profile_pic'] == False:
                dish.profile_pic = Dish._meta.get_field('profile_pic').get_default()

            #save the dish and then save the many-to-many data from the form
            dish.save()
            
            # If your model has a many-to-many relation and you specify commit=False 
            # when you save a form, Django cannot immediately save the form data for 
            # the many-to-many relation. Manually save many-to-many data
            form.save_m2m() 

            # redirect to the dish details page for the newly created dish
            return redirect(f'/dish/{dish.id}')
    
    else: #this is a GET request so create a blank form
        form = DishForm(instance=dish)
    
    context = {
        'user': user,
        'form': form,
        'action': 'new',  #use the 'action' key in the template to determine if the form's action should be new or update
    }
    return render(request,'dish/dish.html', context)

@login_required
def rate_dish(request, dish_id):
    # This view can be called via Ajax and returns only the ratings form

    user = request.user #User.objects.get(id=request.session['user_id'])
    dish = Dish.objects.get(id=dish_id)

    # print(f'Processing rating of dish {dish.title} by {user.full_name()}')
    if request.method == 'POST':

        rating = Rating(user=user, dish=dish)
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            rating = form.save()
            # return redirect(f'/dish/{dish_id}')
    
    else: #this is a GET request so return to the dish details page where the blank rating form is displayed
        return redirect(f'/dish/{dish.id}')
    
    if hasattr(dish,'ratings'):
        # if user has rated dish, don't let user rate it again
        # get user's rating for this dish
        if dish.ratings.filter(user=user).count() > 0:
            user_has_rated_dish = True
            user_rating_this_dish = dish.ratings.filter(user=user).first()
            form = None #don't return a form

        else:
            user_has_rated_dish = False
            user_rating_this_dish = None

        #recalculate average ratings
        average_rating = Rating.objects.filter(dish=dish).aggregate(Avg('rating'))['rating__avg'] or 0
        all_ratings = dish.ratings.all()

    else:
        average_rating = 0
        all_ratings = None

    context = {
        'user': user,
        'dish': dish,
        'average_rating': average_rating,
        'all_ratings': all_ratings,
        'user_has_rated_dish': user_has_rated_dish,
        'user_rating_this_dish': user_rating_this_dish,
        'ratings_form': form,
    }
   
    return render(request, 'dish/ratingForm.html', context)

@login_required
def comment_dish(request, dish_id):
    # This view can be called via Ajax and returns only the ratings form

    user = request.user #User.objects.get(id=request.session['user_id'])
    dish = Dish.objects.get(id=dish_id)

    # print(f'Processing rating of dish {dish.title} by {user.full_name()}')
    if request.method == 'POST':

        comment = Comment(user=user, dish=dish)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            # return redirect(f'/dish/{dish_id}')
    
    else: #this is a GET request so return to the dish details page where the blank rating form is displayed
        return redirect(f'/dish/{dish.id}')
    
    if hasattr(dish,'dish_comments'):
        all_comments = dish.dish_comments.all()

    else:
        all_comments = None

    form = CommentForm()

    context = {
        'user': user,
        'dish': dish,
        'all_comments': all_ratings,
        'comments_form': form,
    }
   
    return render(request, 'dish/commentForm.html', context)

@login_required
def update_dish(request, dish_id):
    user = request.user #User.objects.get(id=request.session['user_id'])
    dish = Dish.objects.get(id=dish_id)

    if request.method == 'POST':

        form = DishForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():

            dish = form.save(commit=False)

            # if the user deleted the previous photo, add the default photo
            if form.cleaned_data['profile_pic'] == None or form.cleaned_data['profile_pic'] == False:
                dish.profile_pic = Dish._meta.get_field('profile_pic').get_default()
            
            dish.save()
            
            # If your model has a many-to-many relation and you specify commit=False when you save a form, 
            # Django cannot immediately save the form data for the many-to-many relation.
            # Manually save many-to-many data
            form.save_m2m() 

            return redirect(f'/dish/{dish_id}')
    
    else: #this is a GET request so create a blank form
        form = DishForm(instance=dish)
    
    context = {
        'user': user,
        'form': form,
        'dish': dish,
        'action': 'update',  #use the 'action' key in the template to determine if the form's action should be new or update
    }
    return render(request,'dish/dish.html', context)

def dish_details(request, dish_id):
    # returns dish details page
    # since the ratings form is on the dish details page, code handles rating logic as well
 
    user = request.user # User.objects.get(id=request.session['user_id'])
    dish = Dish.objects.get(id=dish_id)

    if hasattr(dish,'ratings'):

        # determine if this user has rated this dish before
        if dish.ratings.filter(user=user).count() > 0:
            #user hsa rated dish; don't permit another rating (just don't return a form object)
            print(f"Ratings for {dish.title}: {dish.ratings.filter(user=user).count()}")
            user_has_rated_dish = True
            user_rating_this_dish = dish.ratings.filter(user=user).first()
            form = None

        else:
            # user has not yet rated this dish
            user_has_rated_dish = False
            user_rating_this_dish = None
            form = RatingForm()

        #get the oversall ratings for this dish
        average_rating = Rating.objects.filter(dish=dish).aggregate(Avg('rating'))['rating__avg'] or 0
        all_ratings = dish.ratings.all()

    else:
        # dish has no ratings yet
        print(f"No ratings yet for {dish.title}.")
        form = RatingForm()
        average_rating = 0
        all_ratings = None

    context = {
        'user': user,
        'dish': dish,
        'average_rating': average_rating,
        'all_ratings': all_ratings,
        'user_has_rated_dish': user_has_rated_dish,
        'user_rating_this_dish': user_rating_this_dish,
        'form': form,
    }
    return render(request, 'dish/dish-details.html', context)

@login_required
def favorites(request):
    # returns user's  favorite dish

    user = request.user #User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'dish': user.favorite_dishes.all().order_by('date'),
    }
    return render(request, 'dish/favorites.html', context)

@login_required
def favorite(request, dish_id):
    #user has favorited dish

    dish = Dish.objects.get(id=dish_id)
    user = request.user #User.objects.get(id=request.session['user_id'])
    if user not in dish.favorited_by.all():
        dish.favorited_by.add(user)
        dish.save()   #IS THIS NECESSARY?

    # user could be on any numbmer of pages when they push the favorite button
    # return the user to the same page they were on when they favorited the course
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def unfavorite(request, dish_id):
    # user has un-favorited the dish

    dish = Dish.objects.get(id=dish_id)
    user = request.user #User.objects.get(id=request.session['user_id'])
    if user in dish.favorited_by.all():
        dish.favorited_by.remove(user)
        dish.save()   #IS THIS NECESSARY?
    
    # user could be on any numbmer of pages when they push the favorite button
    # return the user to the same page they were on when they favorited the course
    return redirect(request.META.get('HTTP_REFERER'))

def categories(request):
    # displays a page with list of categories
    # user can click on a category link and see all dishes of that category each linked to dishes for  
    user = request.user #User.objects.get(id=request.session['user_id'])
    categories = Category.objects.all()
    context = {
        'user': user,
        'categories' : categories,
    }
    return render(request, 'dish/categories.html', context)

@staff_member_required
def get_category(request):

    user = request.user #User.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dish/categories')
    
    else: #this is a GET request so create a blank form
        form = CategoryForm()
    
    context = {
        'user': user,
        'form': form,
        'action': 'new', #use the 'action' key in the template to determine if the form's action should be new or update
    }
    return render(request,'dish/category.html', context)

@staff_member_required
def update_category(request, category_id):

    user = request.user #User.objects.get(id=request.session['user_id'])
    category = Category.objects.get(id=category_id)

    if request.method == 'POST':

        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            return redirect(f'/category/{category_id}')
    
    else: #this is a GET request so create an update form
        form = CategoryForm(instance=category)
    
    context = {
        'user': user,
        'form': form,
        'category': category,
        'action': 'update',  #use the 'action' key in the template to determine if the form's action should be new or update
    }
    return render(request,'dish/category.html', context)

def category_dishes(request, category_id):
    # returns dishes for a particular category
    user = request.user #User.objects.get(id=request.session['user_id'])
    category = Category.objects.get(id=category_id)
    context = {
        'user': user,
        'category' : category,
        'dishes': category.dishes.all().order_by('rating__rating'),
    }
    return render(request, 'classes/interest-classes.html', context)

def search_dishes(request):
    query = request.GET.get('q', '') #get the search criterial from the querystring (or '' if it doesn't exist)
    print("SEARCHING FOR: ", query)
    if query:
        queryset = (Q(title__icontains = query)) | (Q(description__icontains=query)) | (Q(ingredients__icontains=query)) | (Q(instructions__icontains=query))
        # Q(poster__username__icontains = query) | Q(categories__name__icontains = query)
        dishes = Dish.objects.filter(queryset).distinct().order_by('date')
        print("DISHES: ", dishes)
    else:
        dishes = Dish.objects.all().order_by('date')

    # paginator = Paginator(dishes, DISHSES_PER_PAGE) #show 9 dishes per page
    # page_number = request.GET.get('page') or 1
    # page_obj = paginator.get_page(page_number)

    context = {
        'user': request.user, #User.objects.get(id=request.session['user_id']),
        # 'page_obj': page_obj,
        'dishes': dishes, #page_obj.object_list,
        # 'current_page': page_number,
        'search_query': query,
    }
    return render(request, 'dish/card-dish.html', context)

def made_it(request, dish_id):
        pass   