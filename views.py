from django.http import HttpResponse, Http404
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.conf import settings
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *

import clef
import math
import re

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

def loginview(request):
	context = {}
	if request.user.is_authenticated():
		if 'returnto' in request.GET:
			url = request.GET['returnto']
		else:
			url = reverse('blog:index')
		messages.add_message(request, messages.ERROR, "You're already logged in!")
		return redirect(url)
	else:
		if request.method == 'GET':
			return render(request, 'blog/login.html', context)
		else:
			if 'username' in request.POST and 'password' in request.POST:
				u = authenticate(username=request.POST['username'], password=request.POST['password'])

				if u != None:
					if u.is_active:
						login(request, u)
						if 'returnto' in request.POST:
							url = request.POST['returnto']
						else:
							url = reverse('blog:index')
						messages.add_message(request, messages.SUCCESS, "Logged in as %s" % u.username)
						return redirect(url)
					else:
						messages.add_message(request, messages.ERROR, "This user has been banned. If you think this is wrong, message the administrator.")
				else:
					messages.add_message(request, messages.ERROR, "This username/password combination is invalid.")
				return render(request, 'blog/login.html', context)

def registerview(request):
	context = {}
	if request.user.is_authenticated():
		if 'returnto' in request.GET:
			url = request.GET['returnto']
		else:
			url = reverse('blog:index')
		messages.add_message(request, messages.ERROR, "You're already logged in!")
		return redirect(url)
	else:
		if request.method == 'GET':
			return render(request, 'blog/register.html', context)
		else:
			if 'returnto' in request.POST:
				url = request.POST['returnto']
			else:
				url = reverse('blog:index')
			if 'username' in request.POST and 'password' in request.POST and 'passwordconfirm' in request.POST:
				if not request.POST['username'] or not request.POST['password'] or not request.POST['passwordconfirm']:
					messages.add_message(request, messages.ERROR, "All fields are required")
					return render(request, 'blog/register.html', context)
				else:
					if bool(re.compile('[^a-zA-Z0-9\_\+\.\-]+').search(request.POST['username'].strip())) or len(request.POST['username'].strip()) > 30:
						messages.add_message(request, messages.ERROR, "Invalid username")
						return render(request, 'blog/register.html', context)
					try:
						if request.POST['password'] != request.POST['passwordconfirm']:
							messages.add_message(request, messages.ERROR, "Passwords don't match")
							return render(request, 'blog/register.html', context)
						u = User.objects.create_user(request.POST['username'].strip(), '', request.POST['password'])
					except:
						messages.add_message(request, messages.ERROR, "Username already in use")
						return render(request, 'blog/register.html', context)
					else:
						messages.add_message(request, messages.SUCCESS, "Successfully registered %s. You can now login." % request.POST['username'])
						return redirect(url)
			else:
				messages.add_message(request, messages.ERROR, "All fields are required")
				return render(request, 'blog/register.html', context)
	

def logoutview(request):
	if request.user.is_authenticated():
		logout(request)
		messages.add_message(request, messages.SUCCESS, "Logged out.")
	else:
		messages.add_message(request, messages.ERROR, "You're not logged in!")
	if 'returnto' in request.GET:
		return redirect(request.GET['returnto'])
	else:
		return redirect(reverse('blog:index'))

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

def postcomment(request):
	toreturn = {}
	if request.method == "POST":
		if request.user.is_authenticated():
			if request.POST['comment-to-submit'] != "":
				if 'reply-to' in request.POST:
					comment = get_object_or_404(Comment, id=request.POST['reply-to'])
					c = Comment(body=request.POST['comment-to-submit'], user=request.user, reply_to=comment)
				elif 'parent' in request.POST:
					parent = get_object_or_404(Post, id=request.POST['parent'])
					c = Comment(body=request.POST['comment-to-submit'], user=request.user, parent=parent)
				c.save()
				messages.success(request, "Successfully commented!")
			else:
				messages.error(request, "Comment can't be empty!")
		else:
			messages.error(request, "You need to log in to comment!")
		return redirect(request.META['HTTP_REFERER'])