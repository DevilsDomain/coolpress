from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from pip._internal.utils.misc import enum


class Category(models.Model):
    label = models.CharField(max_length=200)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.label} ({self.id})'


class CoolUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gravatar = models.URLField()
    github_profile = models.URLField()
    github_repositories = models.IntegerField(null=True)


class poststatus:
    DRAFT = 'DRAFT'
    PUBLISHED = 'PUBLISHED'


class Post(models.Model):
    title = models.CharField(max_length=400)
    body = models.TextField()
    image_link = models.URLField()
    status = models.CharField(max_length=32,
                              choices=[(poststatus.DRAFT, 'Draft'), (poststatus.PUBLISHED, 'Published')],
                              default=poststatus.DRAFT)
    author = models.ForeignKey(CoolUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}'
