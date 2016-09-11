from django import template
import markdown2

register = template.Library()

@register.filter(name='markdown')
def markdown(value):
	return markdown2.markdown(value, extras=['fenced-code-blocks'])

@register.filter(name='word_count')
def word_count(value):
	return len(value.split(" "))

@register.filter(name='tobootstrap')
def tobootstrap(value):
	return {
		'error': 'danger',
		'warning': 'warning',
		'info': 'info',
		'success': 'success',
	}[value.lower()]
