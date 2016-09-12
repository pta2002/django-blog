from django import template
from django.conf import settings
from django.utils.html import mark_safe
from urllib.parse import urlparse
import markdown2, bleach

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

@register.simple_tag
def google_analytics():
    trackingcode = getattr(settings, "GOOGLE_ANALYTICS_TRACKINGCODE", '')
    if trackingcode == '':
        return ''
    return mark_safe("""<script>
              (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
              (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
              m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
              })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

              ga('create', '%s', 'auto');
              ga('send', 'pageview');

            </script>""" % trackingcode)
