from django.contrib import admin

from e_mall.models.products import Products 
from e_mall.models.userprofile import *
from e_mall.models.category import Category 
from e_mall.models.location import *


admin.site.register(Products)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Country)
admin.site.register(Profile)
admin.site.register(ProfileFollow)
admin.site.register(Subscription)
admin.site.register(SubscriptionPlan)
admin.site.register(Advertisements)