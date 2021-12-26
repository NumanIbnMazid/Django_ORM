from django import template
from django.db.models.query import QuerySet

register = template.Library()


@register.filter
def get_type(value):
    return type(value)

@register.filter
def is_list(value):
    if isinstance(value, QuerySet) or isinstance(value, list):
        return True
    return False
