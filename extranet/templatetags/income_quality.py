import json
import os
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_income_quality(income_quality, voucher):
    heading = {}
    with open(os.path.join(settings.EXTRANET_DIR, 'quality_headings.json'), 'r') as quality_headings:
        heading = json.load(quality_headings)

    ITEM_LIMIT = 15

    ticket = [ticket for ticket in income_quality if ticket['ticket'] == voucher][0]
    species_headings = heading[0][ticket['species']]
    
    details = {}

    for i in range(1, ITEM_LIMIT+1):
        if ticket[f'item_{i}']:
            details[species_headings[f'item_{i}']] = {
                'percentage': ticket[f'item_{i}'], 
                'bonus': ticket[f'bonus_item_{i}'], 
                'reduction': ticket[f'reduction_item_{i}']
            }

    response = {
        'gluten': ticket['gluten'],
        'details': details
    }
    
    return response