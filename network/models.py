from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

#https://docs.djangoproject.com/en/3.2/topics/db/models/
class Following(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='followedUser')
    followers = models.ManyToManyField(User, related_name="following")

    @property
    def followersCount(self):
        return self.followers.count()

class Post(models.Model):
    text = models.CharField(max_length=400)
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')
    timestamp = timestamp = models.DateTimeField(default=datetime.now)
    likes = models.ManyToManyField('User', default=None, blank=True, related_name='postLikes')

    @property
    def getLikesCount(self):
        return self.likes.count()