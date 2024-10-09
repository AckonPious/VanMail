from django import template
from authentication.models import Location

register = template.Library()

@register.simple_tag(takes_context=True)
def get_locations(context):
    request = context['request']
    user_location = request.user.location

    # Exclude the current user's location
    if request.user.is_authenticated and request.user.is_admin:
        locations = Location.objects.all()
    else:
        locations = Location.objects.exclude(id=user_location.id)

    return locations