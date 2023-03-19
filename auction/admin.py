from django.contrib import admin
from .models import *


# Register your models here.
models_list = [Condition, Product, ProductImage, Auction, Bid]
for model in models_list:
    admin.site.register(model)
