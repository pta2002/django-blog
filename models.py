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

    def __str__(self):
    	return self.post_title

    class Meta:
    	permissions = (
    			("view_drafts", "View anyone's drafts"),
    		)


class Comment(models.Model):
    parent = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_to = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    pub_date = models.DateTimeField('date published', default=timezone.now)
    edit_date = models.DateTimeField('date editted', default=timezone.now)
    body = models.TextField(blank=False)

    def __str__(self):
        return self.body[:100] + "..."

    class Meta:
        permissions = (
            ("edit_comments", "Edit anyone's comments"),
        )