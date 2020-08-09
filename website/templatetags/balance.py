from django import template

register = template.Library()

@register.simple_tag
def balance(records):
    initial_balance = records[0]
    final_balance = records[-1]
    return {
        'initial_page_balance': initial_balance['row_balance'] - initial_balance['amount_sign'],
        'final_page_balance': final_balance['row_balance']
    }