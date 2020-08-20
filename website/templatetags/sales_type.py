from django import template

register = template.Library()

@register.simple_tag
def get_sales_type(indicator):
    title = None
    class_name = None
    if indicator == '2':
        title = 'VENTAS'
        class_name = 'sales'
    elif indicator == '2B':
        title = 'A FIJAR'
        class_name = 'to-fix'
    else:
        title = 'OTROS'
        class_name = 'others'
    return {
        'title': title,
        'class': class_name
    }