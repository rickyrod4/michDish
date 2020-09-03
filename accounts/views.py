from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from dish.models import *
from django.contrib import messages

def signup(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    
    else:
        form = SignUpForm()
    
    return render(request, 'registration/signup.html', {'form': form})

def user_profile(request,profiled_user_id):
    profiled_user = User.objects.get(id=profiled_user_id)
    location = profiled_user.profile.location or ''

    average_rating = Rating.objects.filter(user=profiled_user).aggregate(Avg('rating'))['rating__avg'] or 0
    all_ratings = profiled_user.ratings.all()

    context = {
        'user': request.user,
        'profiled_user': profiled_user,
        'location': location,
        'user_average_rating' : average_rating,
        'all_ratings' : all_ratings,
    }
    return render(request, 'registration/user-profile.html', context)

def update_user_profile(request, profiled_user_id):
    profiled_user = User.objects.get(id=profiled_user_id)
    profile = profiled_user.profile

    if request.method == 'POST':

        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():

            profile = form.save(commit=False)

            # if the user deleted the previous photo, add the default photo
            if form.cleaned_data['profile_pic'] == None or form.cleaned_data['profile_pic'] == False:
                profile.profile_pic = UserProfile._meta.get_field('profile_pic').get_default()

            #save the profile and then save the many-to-many data from the form
            profile.save()

            # If your model has a many-to-many relation and you specify commit=False when you save a form, 
            # Django cannot immediately save the form data for the many-to-many relation.
            # Manually save many-to-many data
            form.save_m2m() 

            return redirect(f'/registration/{profiled_user_id}')
    
    else: #this is a GET request so create a blank form
        form = UserProfileForm(instance=profile)
    
    context = {
        'user': request.user,
        'profiled_user': profiled_user,
        'form': form,
    }
    return render(request,'registration/user-profile-form.html', context)

