import iso8601
from datetime import datetime

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter
@stringfilter
def date_string(value):
    return  iso8601.parse_date(value)
