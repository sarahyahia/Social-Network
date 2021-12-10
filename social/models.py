from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver



class Post(models.Model):
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    body       = models.TextField()
    created_at = models.DateTimeField(default = timezone.now)
    likes      = models.ManyToManyField(User, blank=True, related_name="likes")
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    
    class Meta:
        ordering = ('-created_at',)



class Comment(models.Model):
    comment    = models.TextField()
    post       = models.ForeignKey(Post, on_delete=models.CASCADE)
    author     = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default = timezone.now)
    
    class Meta:
        ordering = ('created_at',)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateTimeField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.png', blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance,**kwargs):
    instance.profile.save()
    



class Notification(models.Model):
    # like= 1 comment =2 , follow =3
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, related_name="notification_to", on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)