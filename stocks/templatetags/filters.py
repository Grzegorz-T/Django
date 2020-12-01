from django import template

register = template.Library()

@register.filter
def isnt_empty(dictionary, key):
    if(dictionary.get(key)):
        return True
    else:
        return False

@register.filter   
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag
def get_value(dictionary, key, value):
    return dictionary.get(str(key))[value]

