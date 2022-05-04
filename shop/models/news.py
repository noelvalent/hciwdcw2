from django.db import models
from django.utils import timezone

from .store import Store
from .event import Event


class News(models.Model):
    """
    This is NEWS Model.
    Actually it is not used directly.
    It is used as abstract model.

    [Schema]
    News
    ID | FEATURED_IMAGE | TITLE | POSTER | CONTENT | PUBLISHED_BY

    """
    featured_image = models.ImageField(upload_to='img', help_text='Image to show in list', blank=True, null=True)
    title = models.CharField(max_length=256, help_text='News title e.g. Deal title or Update title')
    poster = models.ImageField(upload_to='img', help_text='Image to show in content page')
    content = models.TextField(help_text='News Contents')
    published_by = models.DateTimeField(default=timezone.now, help_text='Published date')

    class Meta:
        abstract = True


class Deal(News):
    """
    It is Deal Model.
    It is stored promotion information.
    It is similar with News but include two fks.

    [Schema]
    Deal
    ID | FEATURED_IMAGE | TITLE | POSTER | CONTENT | PUBLISHED_BY | RELATED_STORE | EVENT

    """
    related_store_id = models.ForeignKey(Store, on_delete=models.DO_NOTHING, help_text='Event Store')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, help_text='Event Schedule')

    def get_format_datetime(self):
        return self.published_by.strftime('%d.%b.%Y')

    def __str__(self):
        return self.title

class Announce(News):
    """
    It is Announce Model.
    It is stored news from the stores.
    Not different from News

    [Schema]
    Announce
    ID | FEATURED_IMAGE | TITLE | POSTER | CONTENT | PUBLISHED_BY
    """
    pass

