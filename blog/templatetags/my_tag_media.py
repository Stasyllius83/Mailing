from django import template
from django.templatetags.static import static
register = template.Library()

@register.filter(name="mediapath")
def mediapath(value):
    if value:
        return value.url
    return static('/img/no_image.png')
