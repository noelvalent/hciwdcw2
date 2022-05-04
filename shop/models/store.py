from django.db import models
from django.utils.translation import gettext_lazy as _


class Store(models.Model):
    """
    This is NEWS Model.
    Actually it is not used directly.
    It is used as abstract model.

    [Schema]
    News
    ID | LOGO | NAME | STORE_TYPE | LOCATION | CONTACT | OPENING | DESCRIPTION

    """

    class StoreType(models.TextChoices):
        """
        This is StoreType class.
        It will be used as TextChoices for ChoiceFiled like Enum.
        """
        BANK = 'BNK', _('Bank')
        BEAUTY = 'BUT', _('Beauty')
        ELECTRICAL = 'ECT', _('Electrical')
        ENTERTAINMENT = 'ENT', _('Entertainment')
        FASHION = 'FSH', _('Fashion')
        FOOD = 'FOD', _('Food')
        FURNITURE = 'FUN', _('Furniture')
        JEWELLERY = 'JEW', _('Jewellery')
        SERVICES = 'SVC', _('Services')
        SPORTS = 'SPT', _('Sport')
        TOY = 'TOY', _('Toy')

    logo = models.ImageField(upload_to='img', help_text='This is Logo image')
    name = models.CharField(max_length=256, help_text='Store name')
    store_type = models.CharField(
        max_length=3,
        help_text='Store Type',
        choices=StoreType.choices,
        default=StoreType.FOOD
    )
    location = models.CharField(max_length=256, help_text='Store location')
    contact = models.CharField(max_length=256, help_text='Store contact')
    opening = models.CharField(max_length=256, help_text='Opening Time')
    description = models.TextField(help_text='Store description')

    def __str__(self):
        return self.name
