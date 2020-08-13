from django import template

register = template.Library()

@register.simple_tag
def get_totals(totals_list, species_title, field):
    for total in totals_list:
        if total['field_description'] == field and total['species_title'] == species_title:
            return total