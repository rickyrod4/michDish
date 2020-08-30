from django.urls import path
from django.contrib.auth import views as aut_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('<int:profiled_user_id>', views.user_profile, name="user_profile"),
    path('<int:profiled_user_id>/update', views.update_user_profile, name="update_user_profile"),

]