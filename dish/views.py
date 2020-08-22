from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
# from login_app.models import User
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.db.models import Avg, F, Q
from django.core.paginator import Paginator
import math
from zxcvbn import zxcvbn

DISHES_PER_PAGE = 6


# Create your views here.
def index(request):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')
    
    dishes = Dish.objects.all() #.order_by('date')

    paginator = Paginator(dishes, DISHES_PER_PAGE) # NUMBER OF dishes per page TO DISPLAY
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    context = {
        #'user': User.objects.get(id=request.session['user_id']),
        'page_obj': page_obj,
        'current_page': page_number,
    }
    return render(request, 'dishes/dashboard.html', context)

def get_dish(request):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    dish = Dish(creator=user) #create a new Dish object with the current user as the creator

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
        dish = DishForm(instance=dish)
    
    context = {
        'user': user,
        'form': form,
        'action': 'new',
    }
    return render(request,'dishes/dish.html', context)

def rate_dish(request, dish_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    dish = Dish.objects.get(id=dish_id)

    print(f'Processing rating of dish {dish.title} by {user.full_name()}')
    if request.method == 'POST':

        rating = Rating(user=user, dish=dish)
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            rating = form.save()
            # return redirect(f'/dishes/{dish_id}')
    
    else: #this is a GET request so return to the dish details page where the blank rating form is displayed
        return redirect(f'/dishes/{dish.id}')
    
    if hasattr(dish,'ratings'):
        if dish.ratings.filter(user=user).count() > 0:
            user_has_rated_dish = True
            user_rating_this_dish = dish.ratings.filter(user=user).first()
            form = None

        else:
            user_has_rated_dish = False
            user_rating_this_dish = None

        average_rating = Rating.objects.filter(dish=dish).aggregate(Avg('number_of_stars'))['number_of_stars__avg'] or 0
        temp_avg = math.floor(average_rating)
        temp_rating = Rating(user=user, dish=dish, number_of_stars = temp_avg)
        average_rating_text = temp_rating.get_number_of_stars_display()
        all_ratings = dish.ratings.all()

    else:
        average_rating = 0
        average_rating_text = ''
        all_ratings = None

    context = {
        'user': user,
        'dish': dish,
        'average_rating': average_rating,
        'average_rating_text' : average_rating_text,
        'all_ratings': all_ratings,
        'user_has_rated_dish': user_has_rated_dish,
        'user_rating_this_dish': user_rating_this_dish,
        'ratings_form': form,
    }
   
    return render(request, 'dishes/ratings-form.html', context)

def update_dish(request, dish_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
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

            return redirect(f'/dishes/{dish_id}')
    
    else: #this is a GET request so create a blank form
        form = DishForm(instance=dish)
    
    context = {
        'user': user,
        'form': form,
        'dish': dish,
        'action': 'update',
    }
    return render(request,'dishes/dish.html', context)

def dish_details(request, dish_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    dish = Dish.objects.get(id=dish_id)

    if hasattr(dish,'ratings'):

        if dish.ratings.filter(user=user).count() > 0:
            print(f"Ratings for {dish.title}: {dish.ratings.filter(user=user).count()}")
            user_has_rated_dish = True
            user_rating_this_dish = dish.ratings.filter(user=user).first()
            form = None

        else:
            user_has_rated_dish = False
            user_rating_this_dish = None
            form = RatingForm()

        average_rating = Rating.objects.filter(dish=dish).aggregate(Avg('number_of_stars'))['number_of_stars__avg'] or 0
        temp_avg = math.floor(average_rating)
        temp_rating = Rating(user=user, dish=dish, number_of_stars = temp_avg)
        average_rating_text = temp_rating.get_number_of_stars_display()
        all_ratings = dish.ratings.all()

    else:
        print(f"No ratings yet for {dish.title}.")
        form = RatingForm()
        average_rating = 0
        average_rating_text = ''
        all_ratings = None

    context = {
        'user': user,
        'dish': dish,
        'average_rating': average_rating,
        'average_rating_text': average_rating_text,
        'all_ratings': all_ratings,
        'user_has_rated_dish': user_has_rated_dish,
        'user_rating_this_dish': user_rating_this_dish,
        'ratings_form': form,
    }
    return render(request, 'dishes/dish-details.html', context)

def favorites(request):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'dish': user.favorite_dishes.all().order_by('date'),
    }
    return render(request, 'dishes/favorites.html', context)

def favorite(request, dish_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    dish = Dish.objects.get(id=dish_id)
    user = User.objects.get(id=request.session['user_id'])
    if user not in dish.favorited_by.all():
        dish.favorited_by.add(user)
        dish.save()   #IS THIS NECESSARY?

    # user could be on any numbmer of pages when they push the favorite button
    # return the user to the same page they were on when they favorited the course
    return redirect(request.META.get('HTTP_REFERER'))

def unfavorite(request, dish_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    dish = Dish.objects.get(id=dish_id)
    user = User.objects.get(id=request.session['user_id'])
    if user in dish.favorited_by.all():
        dish.favorited_by.remove(user)
        dish.save()   #IS THIS NECESSARY?
    
    return redirect(request.META.get('HTTP_REFERER'))

def categories(request):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    categories = Category.objects.all()
    context = {
        'user': user,
        'categories' : categories,
    }
    return render(request, 'dishes/categories.html', context)

def get_category(request):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dishes/categories')
    
    else: #this is a GET request so create a blank form
        form = CategoryForm()
    
    context = {
        'user': user,
        'form': form,
        'action': 'new',
    }
    return render(request,'dishes/category.html', context)


def update_category(request):
    pass

def add_category(request):
    pass

def remove_category(request):
    pass

def category_dishes(request):
    pass

def search_dishes(request):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    query = request.GET.get('q', '')
    print("SEARCHING FOR: ", query)
    if query:
        queryset = (Q(title__icontains = query)) | (Q(description__icontains=query))
        dishes = Dish.objects.filter(queryset).distinct().order_by('date')
        print("DISHES: ", dishes)
    else:
        dishes = Dish.objects.all().order_by('date')

    paginator = Paginator(dishes, DISHSES_PER_PAGE) #show 9 dishes per page
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'page_obj': page_obj,
        'dishes': page_obj.object_list,
        'current_page': page_number,
        'search_query': query,
    }
    return render(request, 'dishes/card-dish.html', context)
    