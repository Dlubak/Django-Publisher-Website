"""publisher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from blog import views


app_name = 'blog'
urlpatterns = [
    # Homepage
    path('', views.index, name='index'),
    # ## ARTICLES ##
    # Page to read article
    path('article/<int:article_id>', views.article, name='article'),
    # New article form
    path('new_article/', views.new_article, name='new_article'),
    # Edit article form
    path('edit_article/<int:article_id>',
         views.edit_article, name='edit_article'),
    # Delete article
    path('delete_article/<int:article_id>',
         views.delete_article, name='delete_article'),
    path('search_article', views.search_article, name="search_article"),
]
