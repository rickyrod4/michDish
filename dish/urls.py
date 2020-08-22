from django.urls import path
from . import views

app_name = 'dish'

urlpatterns = [
    path('', views.index, name="index"),
    path('new', views.get_dish, name='get_dish'),
    path('<int:dish_id>/rate', views.rate_dish, name="rate_dish"),
    path('<int:dish_id>/update', views.update_dish, name="update_dish"),
    path('<int:dish_id>', views.dish_details, name="dish_details"),

    path('<int:dish_id>/favorite', views.favorite, name="favorite"),
    path('<int:dish_id>/unfavorite', views.unfavorite, name="unfavorite"),
    path('categories', views.categories, name="categories"),
    path('categories/new', views.get_category, name="get_category"),
    path('categories/<int:category_id>/update', views.update_category, name="update_category"),
    path('categories/<int:category_id>/add', views.add_category, name="add_category"),
    path('categories/<int:category_id>/remove', views.remove_category, name="remove_category"),
    path('categories/<int:category_id>', views.category_dishes, name="category_dishes"),
    
    path('favorites', views.favorites, name="favorite_dishes"),
    path('search', views.search_dishes, name="search_dishes"),
]