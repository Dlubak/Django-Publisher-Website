from django.shortcuts import render

# Create your views here.
from .models import Article, Category


def index(request):
    articles = Article.objects.all()
    template_name = 'blog/index.html'
    context = {'articles': articles}
    return render(request, 'blog/index.html', context)


def article_detail(request, article_id):
    pass
