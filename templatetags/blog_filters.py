from django import template
import markdown2, re

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

@register.filter(name='linkify')
def linkify(value):
    #TODO: Fix
    regex = re.compile(r'(https?:\\/\\/(www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{2,256}\\.[a-z]{2,4}\\b([-a-zA-Z0-9@:%_\\+.~#?&//=]*))')
    #return regex.sub(r"<a href='\1' target='_blank'>\1</a>", value)
    return value
