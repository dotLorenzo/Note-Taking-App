from django import template
from ..models import Post
import re

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


@register.filter(name="format_category")
def get_categories(data):
	categories = [c.title() for c in data.split(',')]
	return sorted(categories)

@register.filter(name="format_notes")
def format_notes(notes):

	format_pages = re.sub(r"\[p{1}(\d)+\]", r"<b><i>[Page \1]</i></b>", notes)
	return format_pages