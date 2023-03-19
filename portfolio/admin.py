from django.contrib import admin
from .models import *

# Register your models here.
models = [Profile, Career, Post, ]
for model in models:
    admin.site.register(model)
