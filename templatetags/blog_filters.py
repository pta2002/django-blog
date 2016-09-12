from django import template
from urllib.parse import urlparse
import markdown2, re, bleach

register = template.Library()

def external_links(attrs, new=False):
    o = urlparse(attrs['href'])
    if o.netloc != 'pta2002.com':
        attrs['target'] = '_blank'
    return attrs


def handle_pytld(attrs, new=False):
    if not new:  # This is an existing <a> tag, leave it be.
        return attrs

    # If the TLD is '.py', make sure it starts with http: or https:
    href = attrs['href']
    if href.endswith('.py') and not href.startswith(('http:', 'https:')):
        # This looks like a Python file, not a URL. Don't make a link.
        return None

    # Everything checks out, keep going to the next callback.
    return attrs


@register.filter(name='markdown')
def domarkdown(value, safe="escape"):
	return markdown2.markdown(value, extras=['fenced-code-blocks'], safe_mode=safe)

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
    return bleach.linkify(value, callbacks=[external_links, handle_pytld], parse_email=True)
