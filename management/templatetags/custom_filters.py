from django import template

register = template.Library()

@register.filter
def class_name(value):
    """Return the class name of the object."""
    return value.__class__.__name__
