import re

from django import template
from django.core.urlresolvers import reverse, NoReverseMatch

register = template.Library()


@register.simple_tag(takes_context=True)
def active_url(context, url):
    try:
        pattern = '^%s$' % reverse(url)
    except NoReverseMatch:
        pattern = url
    try:
        path = context['request'].path
    except KeyError:
        path = ''
    return u"class=active" if re.search(pattern, path) else ''
