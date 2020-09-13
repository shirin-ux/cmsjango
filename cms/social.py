from django import template

register=template.library

@register.filter
def is_liked(obj,user):
    return user.is_authenticated and obj.likes.filter(user=user)