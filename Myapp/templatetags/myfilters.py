from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
import re
from datetime import datetime
register = template.Library()

def currency(Montant):
    Montant = round(float(Montant), 2)
    return '{:,} DA'.format(Montant).replace(',',' ') 

@register.filter
def Thousand(Montant):
    # Montant = round(float(Montant), 0)

    return '{:,}'.format(Montant).replace(',',' ')

@register.filter
def is_past_datetime(date_value):
    return datetime.now() >= date_value 

register.filter('currency', currency)