from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Movie)
admin.site.register(Genres)
admin.site.register(Review)
admin.site.register(UserProfile)
admin.site.register(LoginTable)

