from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from reader.forms import NewsForm
from .models import Comment, News, Topic
import random

# Create your views here.


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Wrong username or password')
        except:
            messages.error(request, 'Wrong username or password')

    context = {'page': page}
    return render(request, 'reader/login-register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'reader/login-register.html', {'form': form})


def home(request):
    news = News.objects.all()

    latest_news = news[:3]
    random_news = random.sample(list(news), 3)

    topics = Topic.objects.all()

    context = {'latest_news': latest_news,
               'random_news': random_news, 'topics': topics}
    return render(request, 'reader/home.html', context)


def topicPage(request, category):
    topic = Topic.objects.get(name=category)

    news = News.objects.filter(topic=topic)

    latest_news = news[:5] if news.count() >= 5 else news
    random_news = random.sample(list(news), 5) if news.count() >= 5 else news
    trending_news = random.sample(list(news), 3) if news.count() >= 3 else news

    context = {'latest_news': latest_news,
               'random_news': random_news, 'trending_news': trending_news, 'topic': topic}
    return render(request, 'reader/topic-page.html', context)


@staff_member_required
def createArticle(request):
    form = NewsForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        News.objects.create(
            author=request.user,
            topic=topic,
            title=request.POST.get('title'),
            body=request.POST.get('body'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'reader/create-article.html', context)


def newsArticle(request, pk):
    news = News.objects.get(id=pk)
    related_news = News.objects.filter(topic=news.topic)[:2] if len(
        News.objects.filter(topic=news.topic)) >= 2 else News.objects.filter(topic=news.topic)

    other_news = News.objects.all()

    latest_news = other_news[:4] if other_news.count() >= 4 else other_news
    trending_news = random.sample(
        list(other_news), 3) if other_news.count() >= 3 else other_news

    if request.method == 'POST':

        Comment.objects.create(
            news=news,
            author=request.user,
            body=request.POST.get('comment-body'),
        )

    context = {'news': news, 'related_news': related_news,
               'latest_news': latest_news, 'trending_news': trending_news, }
    return render(request, 'reader/news-article.html', context)
