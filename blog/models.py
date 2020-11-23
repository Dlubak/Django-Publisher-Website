from django.db import models
from django.contrib.auth.models import User


# def get_default_category():
#     return Category.objects.get_or_create(name='default')[0]

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=50, unique=True)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # category = models.ForeignKey(
    #     Category, on_delete=models.SET(get_default_category))

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        if len(self.content) >= 30:
            return f"{self.content[:30]}..."
        return self.content


class Comment(models.Model):
    author = models.CharField(max_length=25)
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.body
