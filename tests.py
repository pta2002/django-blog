from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from .models import Post

# Create your tests here.
# You know, I really hate writing these
class HomeViewTests(TestCase):
	def setUp(self):
		randomuser = User.objects.create_user("randomuser", "randomuser@example.com", "temporary")
		randomuser.save()

		authoruser = User.objects.create_user("authoruser", "authoruser@example.com", "temporary")
		authoruser.save()

		alloweduser = User.objects.create_user("alloweduser", "alloweduser@example.com", "temporary")
		alloweduser.user_permissions.add(Permission.objects.get(codename='view_drafts'))
		alloweduser.save()

		draft = Post(post_title="Draft", post_body="Draft post", permalink="draft", published=False, author=authoruser)
		draft.save()

		otherdraft = Post(post_title="Other", post_body="Other post", permalink="odraft", published=False, author=alloweduser)
		otherdraft.save()

		post = Post(post_title="Regular", post_body="Published post", permalink="post", published=True, author=authoruser)
		post.save()

	def test_home_not_logged_in(self):
		response = self.client.get(reverse('blog:index'))
		self.assertQuerysetEqual(response.context['posts'], ['<Post: Regular>'])

	def test_home_randomuser(self):
		self.client.login(username="randomuser", password="temporary")
		response = self.client.get(reverse('blog:index'))
		self.assertQuerysetEqual(response.context['posts'], ['<Post: Regular>'])

	def test_home_author(self):
		self.client.login(username="authoruser", password="temporary")
		response = self.client.get(reverse('blog:index'))
		self.assertQuerysetEqual(response.context['posts'], ['<Post: Regular>', '<Post: Draft>'])

	def test_home_alloweduser(self):
		self.client.login(username="alloweduser", password="temporary")
		response = self.client.get(reverse('blog:index'))
		self.assertQuerysetEqual(response.context['posts'], ['<Post: Regular>', '<Post: Other>', '<Post: Draft>'])

class ViewpostViewTests(TestCase):
	def setUp(self):
		authoruser = User.objects.create_user("author", "author@example.com", "temporary")
		authoruser.save()

		self.post = Post(post_title="Unpublished post", post_body="I am not published", permalink="unpublished",
					published=False, author=authoruser)
		self.post.save()

		superuser = User.objects.create_user("testuser", "superuser@example.com", "temporary")
		superuser.is_superuser = True
		superuser.save()

		randomuser = User.objects.create_user("randomuser", "randomuser@example.com", "temporary")
		randomuser.save()

		alloweduser = User.objects.create_user("alloweduser", "alloweduser@example.com", "temporary")
		alloweduser.user_permissions.add(Permission.objects.get(codename='view_drafts'))
		alloweduser.save()


	def test_view_unpublished_post_no_login(self):
		# This will test if a user that is not logged in can view an unpublished post

		response = self.client.get(reverse('blog:viewpost', kwargs={'permalink': self.post.permalink}))
		self.assertEqual(response.status_code, 404)

	def test_view_unpublished_post_superuser(self):
		# This will test if a superuser can view an unpublished post

		self.client.login(username="testuser", password="temporary")
		response = self.client.get(reverse('blog:viewpost', kwargs={'permalink': self.post.permalink}))
		self.assertEqual(response.status_code, 200)

	def test_view_unpublished_post_alloweduser(self):
		# This will test if a user with the view_drafts permission can view an unpublished post

		self.client.login(username="alloweduser", password="temporary")
		response = self.client.get(reverse('blog:viewpost', kwargs={'permalink': self.post.permalink}))
		self.assertEqual(response.status_code, 200)

	def test_view_unpublished_post_randomuser(self):
		# This will test if any logged in user can view an unpublished post
		self.client.login(username="randomuser", password="temporary")
		response = self.client.get(reverse('blog:viewpost', kwargs={'permalink': self.post.permalink}))
		self.assertEqual(response.status_code, 404)

	def test_view_unpublished_author(self):
		# This will test if the author can view his drafts

		self.client.login(username="author", password="temporary")
		response = self.client.get(reverse('blog:viewpost', kwargs={'permalink': self.post.permalink}))
		self.assertEqual(response.status_code, 200)
