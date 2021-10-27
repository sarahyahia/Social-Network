from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Post(models.Model):
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    body       = models.TextField()
    created_at = models.DateTimeField(default = timezone.now)
    
    class Meta:
        ordering = ('-created_at',)



class Comment(models.Model):
    comment    = models.TextField()
    post       = models.ForeignKey(Post, on_delete=models.CASCADE)
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default = timezone.now)
    
    class Meta:
        ordering = ('created_at',)