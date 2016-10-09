from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
from .models import *

# Register your models here.
def make_published(modeladmin, request, queryset):
	queryset.update(published=True)

def make_draft(modeladmin, request, queryset):
	queryset.update(published=False)

class PostAdmin(admin.ModelAdmin):
	list_display = ['post_title', 'author', 'pub_date', 'published']

	search_fields = ['post_title']
	list_filter = ['pub_date', 'published']
	filter_horizontal = ['categories']

	fieldsets = [
		("Post info", {'fields': [('post_title', 'permalink', 'published'), 'post_body', 'author', 'categories']}),
		(None, {'fields': ['pub_date',]})
	]

	actions = [make_published, make_draft]

	def view_on_site(self, obj):
		return reverse('blog:viewpost', kwargs={'permalink': obj.permalink})

class PageAdmin(admin.ModelAdmin):
	list_display = ['page_name']

	search_fields = ['page_name']

	fieldsets = [
		("Page info", {'fields': [('page_name', 'permalink'), 'page_body']}),
	]

	def view_on_site(self, obj):
		return reverse('blog:viewpage', kwargs={'permalink': obj.permalink})

admin.site.register(Post, PostAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(MenuLink)
admin.site.register(Category)