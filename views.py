import math
import re

from django.http import Http404
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from .models import *

def index(request):
    if request.user.has_perm('blog.view_drafts'):
        latest_posts = Post.objects.order_by('-pub_date')
    else:
        latest_posts = Post.objects.filter(Q(published=True) | Q(author=request.user.id)).order_by('-pub_date')
    pages = math.ceil(len(latest_posts)/10)
    return render(request, 'blog/home.html', {'posts': latest_posts[:10], 'pages': pages})

def viewpost(request, permalink):
    post = get_object_or_404(Post, permalink=permalink)
    if post.published or request.user.has_perm('blog.view_drafts') \
        or request.user == post.author:
        return render(request, 'blog/viewpost.html', {'post': post})
    else:
        raise Http404()

def viewpage(request, permalink):
    page = get_object_or_404(Page, permalink=permalink)
    return render(request, 'blog/viewpage.html', {'page': page})

def viewcategory(request, category, page=None):
    #TODO: GET options (?show=[number of posts/page], include all for all posts)
    if not page:
        page = 1
    else:
        page = int(page) # The regex will only match numbers, no need to catch errors.

    if category == "all":
        postset = Post.objects.all()
        category = Category(name="All", link="all")
    else:
        category = get_object_or_404(Category, link=category)
        postset = category.post_set
    if request.user.has_perm('blog.view_drafts'):
        posts = postset.order_by('-pub_date')
    else:
        posts = postset.filter(Q(published=True) | Q(author=request.user.id))\
            .order_by('-pub_date')
    totalposts = len(posts)
    postsperpage = 10
    s = (page-1)*postsperpage
    t = min(page*postsperpage, totalposts)
    pages = math.ceil(totalposts/postsperpage)
    if page > pages:
        return redirect(reverse('blog:categorypage', kwargs={'page': pages, 'category': category.link}))
    return render(request, 'blog/category.html', {'posts': posts[s:t], 'category': category, 'totalposts': totalposts, 'page': page, 'pages': pages})

def accountsettings(request):
    if not request.user.is_authenticated():
        messages.error(request, "You need to log in to view this page")
        return redirect(reverse('blog:login') + '?returnto' + request.path)
    return render(request, 'blog/account.html')
