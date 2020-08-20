from django import template

register = template.Library()

@register.simple_tag
def get_rain_total(year):
    total = 0
    for y in year:
        total = total + y['mmsum']
    return total