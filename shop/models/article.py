from django.db import models
from django.utils import timezone

from ckeditor_uploader.fields import RichTextUploadingField


class Article(models.Model):
    """
    This is Article Model.
    It saved blog article.

    [Schema]
    Article
    ID | FEATURED_IMAGE | TITLE | CONTENT | PUBLISHED_BY

    """

    class ArticleType(models.TextChoices):
        """
        This is ArticleType class.
        It will be used as TextChoices for ChoiceFiled like Enum.
        It means Article's Category.
        """
        ANNOUNCE = 'A', 'Announce'
        DELISH = 'D', 'Delish'
        LIFE = 'L', 'Life'
        STORE = 'T', 'Store'
        STYLE = 'S', 'Style'

    featured_image = models.ImageField(upload_to='img', help_text='Image to show in list')
    title = models.CharField(max_length=256, help_text='article title')
    # refer: https://pjs21s.github.io/Ckeditor-image/
    article_type = models.CharField(
        max_length=1,
        help_text='Article Type',
        choices=ArticleType.choices,
        default=ArticleType.ANNOUNCE
    )
    content = RichTextUploadingField()
    published_by = models.DateTimeField(default=timezone.now, help_text='Published date')

    def get_article_type_text(self):
        if self.article_type == 'A':
            return 'Announce'
        elif self.article_type == 'D':
            return 'Delish'
        elif self.article_type == 'L':
            return 'Life'
        elif self.article_type == 'T':
            return 'Store'
        elif self.article_type == 'S':
            return 'Style'
        else:
            return ''

    def get_format_datetime(self):
        return self.published_by.strftime('%d.%b.%Y')

    def __str__(self):
        return self.title
