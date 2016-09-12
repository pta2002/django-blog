from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
from .models import Post, Category, Comment, Page

# Register your models here.
def make_published(modeladmin, request, queryset):
	queryset.update(published=True)

def make_draft(modeladmin, request, queryset):
	queryset.update(published=False)


class CommentInLine(admin.TabularInline):
	model = Comment
	extra = 1
	max_num = 10
	show_change_link = True
	fields = ('user', 'body', 'pub_date')

	def save_model(self, request, obj, form, change):
		obj.edit_date = timezone.now()


class CommentAdmin(admin.ModelAdmin):
	list_display = ['body', 'user', 'pub_date', 'is_top_level']

	def is_top_level(self, obj):
		return obj.parent != None
	is_top_level.boolean = True

	search_fields = ['user', 'pub_date']

	list_filter = ['pub_date']
	inlines = [CommentInLine]

	fieldsets = [
		("Comment info", {'fields': (('body', 'user'), ('parent', 'reply_to'))}),
		("Date Info", {'fields': ('pub_date', 'edit_date')}),
	]

	def save_model(self, request, obj,form, change):
		obj.edit_date = timezone.now()


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
	inlines = [CommentInLine]

	def view_on_site(self, obj):
		return reverse('blog:viewpost', kwargs={'permalink': obj.permalink})

class PageAdmin(admin.ModelAdmin):
	list_display = ['page_name', 'show']

	search_fields = ['page_name']
	list_filter = ['show']

	fieldsets = [
		("Page info", {'fields': [('page_name', 'permalink', 'show'), 'page_body']}),
	]

	def view_on_site(self, obj):
		return reverse('blog:viewpage', kwargs={'permalink': obj.permalink})

admin.site.register(Post, PostAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)