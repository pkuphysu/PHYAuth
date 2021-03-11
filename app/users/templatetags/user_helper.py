from hashlib import md5

from django import template

from ...apply.tasks import get_scopes_information

register = template.Library()


@register.simple_tag(takes_context=True)
def avatar_url(context, size=None, user=None):
    user = context['request'].user if user is None else user
    # return "/static/admin-lte/dist/img/user3-128x128.jpg"
    return 'https://cdn.v2ex.com/gravatar/{hash}?s={size}&d=mm'.format(
        hash=md5(user.get_preferred_email().encode('utf-8')).hexdigest() if user.is_authenticated else '',
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


@register.simple_tag
def model_name(value):
    '''
    Django template filter which returns the verbose name of a model.
    '''
    if hasattr(value, 'model'):
        value = value.model

    return value._meta.verbose_name.title()


@register.simple_tag
def model_name_plural(value):
    '''
    Django template filter which returns the plural verbose name of a model.
    '''
    if hasattr(value, 'model'):
        value = value.model

    return value._meta.verbose_name_plural.title()


@register.simple_tag
def field_name(value, field):
    '''
    Django template filter which returns the verbose name of an object's,
    model's or related manager's field.
    '''
    if hasattr(value, 'model'):
        value = value.model

    return value._meta.get_field(field).verbose_name.title()


@register.filter
def scopes_information(scopes):
    return get_scopes_information(scopes)

# @register.filter(name='add_placeholder')
# def add_placeholder(value, arg, arg2=None):
#     if arg2 is None:
#         return value.as_widget(attrs={'placeholder': arg})
#     else:
#         return value.as_widget(attrs={'placeholder': arg, 'class': arg2})
