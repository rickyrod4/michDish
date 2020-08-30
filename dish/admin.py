from django.contrib import admin
from .models import *

admin.site.register(Dish)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Rating)
admin.site.register(Category)