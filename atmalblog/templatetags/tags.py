from django import template

register = template.Library()


@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        # Home is just '/' so the statement above returns true
        # thus we need to check if the request path is home or not
        if pattern == '/' and request.path == '/':
            return 'active'
        elif pattern == '/':
            return ''
        return 'active'
    return ''
