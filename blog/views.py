from django.contrib.auth.decorators import login_required
# Create your views here.
from authentication.decorators import check_owner_or_admin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ArticleForm, CommentForm
from .models import Article, Comment


def index(request):
    articles = Article.objects.all().order_by('pub_date')
    paginator = Paginator(articles, 2)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template_name = 'blog/index.html'
    context = {'page_obj': page_obj}
    return render(request, template_name, context)


def article(request, article_id):
    template_name = 'blog/article.html'
    article = get_object_or_404(Article, id=article_id)
    form = CommentForm()
    if request.method != 'POST':
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=article
            )
            comment.save()
            print(comment)
    post_comments = Comment.objects.filter(post=article)
    context = {
        'article': article,
        'comments': post_comments,
        'form': form
    }
    print(context)
    return render(request, template_name, context)


@login_required(login_url='/login')
def new_article(request):
    template_name = 'blog/new_article.html'

    if request.method != 'POST':
        articleForm = ArticleForm()
    else:
        articleForm = ArticleForm(request.POST)
        if articleForm.is_valid():
            new_article = articleForm.save(commit=False)
            new_article.author = request.user
            new_article.save()
            return redirect('blog:article', new_article.id)
    context = {'form': articleForm}
    return render(request, 'blog/new_article.html', context)

@check_owner_or_admin
@login_required(login_url='/login')
def edit_article(request, article_id):
    template_name = 'blog/edit.article.html'
    article = get_object_or_404(Article, id=article_id)
    if request.method != 'POST':
        form = ArticleForm(instance=article)
    else:
        form = ArticleForm(instance=article, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:article', article_id=article.id)
    context = {'form': form, 'article': article}
    return render(request, 'blog/edit_article.html', context)


@login_required(login_url='/login')
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.delete()
    return redirect('blog:index')

# TODO: Improve filter by adding more fields to filter from
# Make it more robust


def search_article(request):
    keyword = request.GET.get('query')
    articles = Article.objects.filter(
        title__icontains=keyword).order_by('pub_date')

    paginator = Paginator(articles, 2)
    print(request.get_full_path)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template_name = 'blog/index.html'
    context = {'page_obj': page_obj}
    return render(request, template_name, context)
