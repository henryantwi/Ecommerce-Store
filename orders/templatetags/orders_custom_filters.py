from django import template

register = template.Library()

@register.filter(name='format_currency')
def format_currency(value):
    if isinstance(value, int):
        return '{:,.2f}'.format(value / 100)
    elif isinstance(value, float):
        return '{:,.2f}'.format(value)
    else:
        return value  # Return the value unchanged if it's not an int or float
