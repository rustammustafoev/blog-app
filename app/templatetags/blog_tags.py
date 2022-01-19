"""
Django allows us two helper functions to create a custom template tags:
- simple_tag (Processes and returns a string)
- inclusion_tag (Processes and returns a rendered template)
"""
from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('app/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


# Defining custom filters
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))