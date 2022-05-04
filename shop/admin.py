from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from shop.models import *


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """
    Store admin page with custom image field.
    """

    readonly_fields = ['logo_image']
    list_display = [
        'name',
        'store_type',
    ]

    def logo_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.logo.url,
            width=obj.logo.width,
            height=obj.logo.height,
        ))


class NewsAdmin(admin.ModelAdmin):
    """
    Abstract ModelAdmin for Deal model and Announce model to avoid duplicated code.
    """

    readonly_fields = [
        'featured_image',
        'poster_image'
    ]
    list_display = [
        'title',
    ]

    # Custom readonly fields to show image.
    def featured_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.featured_image.url,
            width=obj.featured_image.width,
            height=obj.featured_image.height,
        ))

    def poster_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.poster.url,
            width=obj.poster.width,
            height=obj.poster.height,
        ))


@admin.register(Deal)
class DealAdmin(NewsAdmin):
    pass


@admin.register(Announce)
class AnnounceAdmin(NewsAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    # custom admin page.
    change_list_template = 'admin/calender.html'

    # == is it deal admin?
    def is_deal_admin(self, request):
        """
        using Http header data, classify deal admin or not.

        Args:
            request:(HttpRequest) current request

        Returns: True | False

        """
        parsed_url = request.path.strip('/').split('/')

        if len(parsed_url) > 2 and parsed_url[2] == 'deal' or request.GET.get('_popup') is not None:
            return True
        else:
            return False

    # set permissions, it can be controlled by only Deal admin.
    def has_add_permission(self, request):
        return self.is_deal_admin(request)

    def has_change_permission(self, request, obj=None):
        return self.is_deal_admin(request)

    def has_delete_permission(self, request, obj=None):
        return self.is_deal_admin(request)

    def changelist_view(self, request, extra_context=None):
        """
        Admin page's default view.
        for customizing, it is override.

        Args:
            request:(HttpRequest) current request
            extra_context:(dict) context data

        """

        import datetime
        import calendar

        from shop.event_calendar import EventCalendar

        # prepared date from GET response.
        after_day = request.GET.get('event_start__gte', None)
        extra_context = extra_context or {}

        # prepare criteria date
        if not after_day:
            d = datetime.date.today()
        else:
            try:
                split_after_day = after_day.split('-')
                d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
            except:
                d = datetime.date.today()

        # get previous month
        previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
        previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
        previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
                                       day=1)  # find first day of previous month

        # get next month
        last_day = calendar.monthrange(d.year, d.month)
        next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
        next_month = next_month + datetime.timedelta(days=1)  # forward a single day
        next_month = datetime.date(year=next_month.year, month=next_month.month, day=1)  # find first day of next month

        # filter data using extra_context
        extra_context['previous_month'] = reverse('admin:shop_event_changelist') + '?event_start__gte=' + str(previous_month)
        extra_context['next_month'] = reverse('admin:shop_event_changelist') + '?event_start__gte=' + str(next_month)

        # create calendar
        cal = EventCalendar()
        html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
        html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
        extra_context['calendar'] = mark_safe(html_calendar)
        return super(EventAdmin, self).changelist_view(request, extra_context)
