from django.contrib import admin
from .models import UserProfile,Post, Comment, Notification
# Register your models here.


admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Notification)