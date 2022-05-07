from django.contrib import admin
from .models import Posts, User, Comments, Follow, Likes

# Register your models here.
admin.site.register(Posts)
admin.site.register(User)
admin.site.register(Comments)
admin.site.register(Follow)
admin.site.register(Likes)
