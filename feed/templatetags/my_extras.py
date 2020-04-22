from django import template

register = template.Library()

@register.filter(name="range")
def times(num):
	'''iterate a range of values'''
	return range(num)

@register.filter(name="rating_difference")
def diff(num):
	''' return the rating remainder from 5. We'll show blank stars for the remainder'''
	if 5-num > 0:
		return range(num-1)