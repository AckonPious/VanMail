from django import template
from authentication.models import Location

register = template.Library()

@register.simple_tag
def get_all_locations():
    return Location.objects.all()  
