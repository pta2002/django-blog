from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Post(models.Model):
    post_title = models.CharField(max_length=200)
    permalink = models.CharField(max_length=100, unique=True)
    post_body = models.TextField('body')
    pub_date = models.DateTimeField('date published', default=timezone.now)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    comments = models.BooleanField(default=True)

    def __str__(self):
    	return self.post_title

    class Meta:
    	permissions = (
    			("view_drafts", "View anyone's drafts"),
    		)

class Page(models.Model):
    page_name = models.CharField(max_length=200)
    permalink = models.CharField(max_length=100, unique=True)
    page_body = models.TextField('body')

    def __str__(self):
        return self.page_name

class MenuLink(models.Model):
    url = models.CharField(max_length=1024)
    text = models.CharField(max_length=200)
    order = models.IntegerField()

    def __str__(self):
        return self.text