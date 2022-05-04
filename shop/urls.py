from django.urls import path

from .views import (
    index,
    about_view,
    contact_view,
    NewsRoomListView,
    NewsRoomDetailView,
    DealListView,
    DealDetailView,
    StoreListView,
    StoreDetailView,
    test
)


app_name = 'shop'

urlpatterns = [
    path('test', test),
    path('', index, name='index'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('event/', DealListView.as_view(), name='deal-list'),
    path('event/<int:pk>/', DealDetailView.as_view(), name='deal-detail'),
    path('news/', NewsRoomListView.as_view(), name='news-list'),
    path('news/<int:pk>/', NewsRoomDetailView.as_view(), name='news-detail'),
    path('store/', StoreListView.as_view(), name='store-list'),
    path('store/<int:pk>/', StoreDetailView.as_view(), name='store-detail'),
]
