from django.shortcuts import render
from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
)

from shop.models import *


# Create your views here.
def page_not_found_view(request, exception):
    """
    Custom 404 Page View
    """
    return render(request, template_name='404.html', status=404)


def test(request):
    return render(request, template_name='404.html', status=404)


def index(request):
    """
    View for Index Page

    Args:
        request:(HttpRequest) current http request

    Returns:
        template render

    """
    return render(request, template_name='index.html', context={'current_page': 0})


def about_view(request):
    """
    View for About Page

    Args:
        request:(HttpRequest) current http request

    Returns:
        template render

    """
    return render(request, template_name='about.html', context={'current_page': 1})


def contact_view(request):
    """
    View for Contact Page

    Args:
        request:(HttpRequest) current http request

    Returns:
        template render

    """
    from django.core.mail import send_mail

    if request.method == 'POST':
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        email = request.POST['email']
        country = request.POST['country']
        subject = request.POST['subject']

        send_mail(
            subject=f'contact from {fname} {lname}',
            message='''first name: {}\nlast name: {}\ncountry: {}\nemail: {}\nsubject:\n{}\n'''.format(
                fname,
                lname,
                country,
                email,
                subject,
            ),
            from_email='dudnspa0203@naver.com',
            recipient_list=['dudnspa0203@naver.com'],
            fail_silently=False
        )

    return render(request, template_name='contact.html', context={'current_page': 5})


class StoreListView(ListView):
    model = Store
    paginate_by = 12
    template_name = 'stores.html'
    context_object_name = 'stores'

    def get_queryset(self):
        q_expr = Q()
        if self.request.GET.get('alpha') is not None:
            if self.request.GET['alpha'].isdigit():
                if self.request.GET['alpha'] == '0':
                    q_expr = q_expr & Q(name__regex=r'^\d')
            else:
                q_expr = q_expr & Q(name__istartswith=self.request.GET['alpha'])

        if self.request.GET.get('category') is not None:
            q_expr = q_expr & Q(store_type=self.request.GET['category'])

        if self.request.GET.get('q') is not None:
            q_expr = q_expr & Q(name__contains=self.request.GET['q'])

        return Store.objects.filter(q_expr).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['current_page'] = 2
        return context


class StoreDetailView(DetailView):
    model = Store
    template_name = 'stores-article.html'
    context_object_name = 'store'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 2
        return context


class DealListView(ListView):
    model = Deal
    paginate_by = 12
    template_name = 'events.html'
    context_object_name = 'deals'

    def get_queryset(self):
        return Deal.objects.order_by('-published_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['current_page'] = 3
        return context


class DealDetailView(DetailView):
    model = Deal
    template_name = 'events-article.html'
    context_object_name = 'deal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 3
        return context


class NewsRoomListView(ListView):
    model = Article
    paginate_by = 12
    template_name = 'news.html'
    context_object_name = 'articles'

    def get_queryset(self):
        q_expr = Q()
        if self.request.GET.get('category') is not None:
            q_expr = Q(article_type=self.request.GET['category'])

        return Article.objects.filter(q_expr).order_by('-published_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['current_page'] = 4
        return context


class NewsRoomDetailView(DetailView):
    model = Article
    template_name = 'news-article.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 4
        return context
