from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Episode)
admin.site.register(Movie)
admin.site.register(Show)

# Register your models here.