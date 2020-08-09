from django import template

register = template.Library()

@register.simple_tag
def download_file(voucher):
    vouchers_pdf = ['LC', 'IC', 'LB', 'IB', 'ND', 'NC', 'FC', 'PC', 'OP', 'RE']

    if voucher.split(' ')[0] in vouchers_pdf:
        return True
    else:
        return False