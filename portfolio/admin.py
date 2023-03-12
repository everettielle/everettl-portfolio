from django.contrib import admin
from .models import *

# Register your models here.
models = [Profile, Post]
for model in models:
    admin.site.register(model)
