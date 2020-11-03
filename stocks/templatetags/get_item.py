from django import template

register = template.Library()

@register.filter
def isnt_empty(dictionary, key):
    if(dictionary.get(str(key))):
        return True
    else:
        return False

@register.simple_tag
def get_value(dictionary, key, value):
    return dictionary.get(str(key))[value]