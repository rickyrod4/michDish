from django.urls import path, include
from . import views

app_name = 'dish'

dish_patterns = [
    path('new', views.get_dish, name='get_dish'),
    path('<int:dish_id>/rate', views.rate_dish, name="rate_dish"),
    path('<int:dish_id>/update', views.update_dish, name="update_dish"),
    path('<int:dish_id>', views.dish_details, name="dish_details"),
    path('<int:dish_id>/favorite', views.favorite, name="favorite"),
    path('<int:dish_id>/unfavorite', views.unfavorite, name="unfavorite"),
    path('<int:dish_id>/made_it', views.made_it, name="made_it"),
]

category_patterns = [
    path('', views.categories, name="categories"),
    path('new', views.get_category, name="get_category"),
    path('<int:category_id>/update', views.update_category, name="update_category"),
    path('<int:category_id>', views.category_dishes, name="category_dishes"),
]

urlpatterns = [
    path('', views.index, name="index"),
    path('dish/', include(dish_patterns)),
    path('category/', include(category_patterns)),
    path('favorites', views.favorites, name="favorite_dishes"),
    path('search', views.search_dishes, name="search_dishes"),
]