from hashlib import md5

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def avatar_url(context, size=None, user=None):
    user = context['request'].user if user is None else user
    # return "/static/admin-lte/dist/img/user3-128x128.jpg"
    return 'https://cdn.v2ex.com/gravatar/{hash}?s={size}&d=mm'.format(
        hash=md5(user.email.encode('utf-8')).hexdigest() if user.is_authenticated else '',
        size=size or '',
    )


@register.simple_tag
def form_mod(field, classes=None, placeholder=None):
    attr = {}
    if classes is not None:
        attr.update({'class': classes})
    if placeholder is not None:
        attr.update({'placeholder': placeholder})
    return field.as_widget(attrs=attr)

# @register.filter(name='add_class')
# def add_class(value, arg="form-control"):
#     return value.as_widget(attrs={'class': arg})
#
#
# @register.filter(name='add_placeholder')
# def add_placeholder(value, arg, arg2=None):
#     if arg2 is None:
#         return value.as_widget(attrs={'placeholder': arg})
#     else:
#         return value.as_widget(attrs={'placeholder': arg, 'class': arg2})
