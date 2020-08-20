from django import template

register = template.Library()

@register.simple_tag
def get_totals(reg_type, totals_list, species_title, filter_field):
    if reg_type == 'deliveries':
        field = 'field_description'
    elif reg_type == 'sales':
        field = 'indicator'
    
    for total in totals_list:
        if total[field] == filter_field and total['species_title'] == species_title:
            return total