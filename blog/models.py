from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=50, unique=True)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_article.png',
                              upload_to='blog')

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        if len(self.content) >= 30:
            return f"{self.content[:30]}..."
        return self.content

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        # 900x300
        if img.height > 300 or img.width > 900:
            output_size = (300, 900)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.body
