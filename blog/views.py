from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Article, Category
from .forms import ArticleForm


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


def new_article(request):
    template_name = 'blog/new_article.html'
    if request.method != 'POST':
        articleForm = ArticleForm()
    else:
        articleForm = ArticleForm(request.POST)
        if articleForm.is_valid():
            new_article = articleForm.save(commit=False)
            new_article.save()
            return redirect('blog:article', new_article.id)
    context = {'form': articleForm}
    return render(request, 'blog/new_article.html', context)
