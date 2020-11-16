from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Article, Category


def index(request):
    articles = Article.objects.all()
    template_name = 'blog/index.html'
    context = {'articles': articles}
    return render(request, template_name, context)


def article(request, article_id):
    template_name = 'blog/article.html'
    article = get_object_or_404(Article, id=article_id)
    context = {'article': article}
    return render(request, template_name, context)


def new article(request):
    template_name = 'blog/new_article.html'
