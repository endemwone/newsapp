from django import template
import requests
import datetime

from reader.models import News, Topic

register = template.Library()


@register.simple_tag
def quote():
    response = requests.get('https://api.quotable.io/random')

    if (response.status_code == 200):
        return response.json()['content']


@register.simple_tag
def date():
    today = datetime.date.today()

    return today.strftime("%a, %B %d, %Y")


@register.simple_tag
def topics():
    return Topic.objects.all()


@register.simple_tag
def news():
    news = News.objects.all()[:3]
    return news
