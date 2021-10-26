from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class News(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name_plural = 'News'

    def __str__(self):
        return self.body[:150]


class Comment(models.Model):
    news = models.ForeignKey(
        News, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.news.title, self.author)
