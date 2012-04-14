from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='lspace')
@stringfilter
def lspace(value):
    return value.replace('\n', '\n    ')
