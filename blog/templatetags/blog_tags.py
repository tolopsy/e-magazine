from django import template
from django.db.models import Count
from blog.models import Category, Post

register = template.Library()


@register.inclusion_tag('partials/category_bar.html')
def show_categories():
	categories = Category.objects.filter(parent=None).order_by('order')
	return {'categories':categories}

@register.simple_tag
def breaking_news():
	breaking_news = Post.publishee.filter(breaking=True)
	return breaking_news


@register.simple_tag
def editor_pick():
	editor_pick = Post.publishee.filter(editor_pick=True)
	return editor_pick

@register.simple_tag
def popular_news():
	popular_news = Post.publishee.filter(popular=True)
	return popular_news

@register.simple_tag
def trending_news():
	trending_news = Post.publishee.filter(trending=True)
	return trending_news

@register.inclusion_tag('partials/newsletter.html')
def newsletter():
	categories = Category.objects.all()
	return {'categories': categories}

@register.inclusion_tag('base.html')
def subscriber_preference():
	categories = Category.objects.all()
	return {'categories': categories}

@register.simple_tag
def company_name():
	return 'Tidings'

@register.simple_tag
def company_email():
	return 'Company E-mail'