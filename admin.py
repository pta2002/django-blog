from django.contrib import admin
from django.urls import reverse
from .models import Post, Category

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

admin.site.register(Post, PostAdmin)
admin.site.register(Category)