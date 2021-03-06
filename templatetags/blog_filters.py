from django import template
from django.conf import settings
from django.utils.html import mark_safe
from urllib.parse import urlparse
import markdown, bleach

from blog.models import Post, Page

register = template.Library()

def external_links(attrs, new=False):
    o = urlparse(attrs['href'])
    if o.netloc != 'pta2002.com':
        attrs['target'] = '_blank'
    return attrs


def internal_links(attrs, new=False):
    href = attrs['href']
    if href.startswith('page:'):
        attrs['href'] = reverse('blog:viewpage', href[5:])
    elif href.startswith('post:'):
        attrs['href'] = reverse('blog:viewpost', href[5:])
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

@register.simple_tag(name='disqus_comments')
def disqus_comments(url, identifier, title):
    disqus_shortname = getattr(settings, 'DISQUS_SHORTNAME', '')
    if disqus_shortname != '':
        return mark_safe("""<div id="disqus_thread"></div>
    <script>
        
        var disqus_config = function () {
            this.page.url = "%s";
            this.page.identifier = "%s";
            this.page.title = "%s";
        };
        
        (function() {  // REQUIRED CONFIGURATION VARIABLE: EDIT THE SHORTNAME BELOW
            var d = document, s = d.createElement('script');
            
            s.src = '//%s.disqus.com/embed.js';
            
            s.setAttribute('data-timestamp', +new Date());
            (d.head || d.body).appendChild(s);
        })();
    </script>
    <noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript" rel="nofollow">comments powered by Disqus.</a></noscript>""" % (url, identifier, title, disqus_shortname))
    else:
        return ''

@register.filter(name='markdown')
def domarkdown(value, safe="escape"):
    if not safe:
        return markdown.markdown(value, extensions=['markdown.extensions.extra', 'markdown.extensions.admonition', 'markdown.extensions.codehilite'], safe_mode=safe)
    else:
        return markdown.markdown(value, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'], safe_mode=safe)

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
    return bleach.linkify(value, callbacks=[external_links, handle_pytld, internal_links], parse_email=True)

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
