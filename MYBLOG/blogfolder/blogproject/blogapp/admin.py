from django.contrib import admin
from .models import BlogPost
from .models import Profile

admin.site.register(BlogPost)
admin.site.register(Profile)
