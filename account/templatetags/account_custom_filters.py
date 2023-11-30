from django import template

register = template.Library()

@register.filter(name='format_currency')
def format_currency(value):
    if isinstance(value, int):
        return '{:,.2f}'.format(value / 100)
    elif isinstance(value, float):
        return '{:,.2f}'.format(value)
    else:
        return value
    
@register.filter(name='get_first_name')
def get_first_name(full_name):
    return full_name.split()[0] if full_name else ''