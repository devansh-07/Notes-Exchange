from django import template
from urllib.parse import urlencode

register = template.Library()

@register.simple_tag
def urlparams(*_, **kwargs):
    safe_args = {k: v for k, v in kwargs.items() if v is not None}
    if safe_args:
        return '?{}'.format(urlencode(safe_args))
    return ''

@register.filter(name='exclude')
def exclude(l, curr_req):
    return l.exclude(id=curr_req.id)

@register.filter(name='order')
def order(l, arg):
    return l.order_by(arg)
