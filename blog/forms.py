from django import forms
from django.forms import Textarea
from blog.models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']


class CommentForm(forms.Form):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            "body": Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Leave a comment!"
                })
        }
