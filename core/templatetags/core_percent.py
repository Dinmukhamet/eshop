from django import template
from decimal import *

register = template.Library()


@register.filter()
def divide(n1, n2):
    try:
        return n1 / n2
    except ZeroDivisionError:
        return None


@register.filter()
def percentof(amount, total):
    # amount, total = args.split(',')
    try:
        return '{:.2f}%'.format(amount/total * 100)
    except ZeroDivisionError:
        return None
