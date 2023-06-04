from django.urls import path
from .views import News, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, Search, \
    CategoryListView, subscribe_to_category, unsubscribe_from_category, CategoryDetailView
from django.views.decorators.cache import cache_page

# from .views import index

app_name = 'news'
urlpatterns = [
    # path('', cache_page(60 * 1)(News.as_view())),
    path('', News.as_view()),
    # path('', index, name='index'),
    # path('<int:pk>/', cache_page(60 * 5)(PostDetailView.as_view()), name='post_detail'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('edit/<int:pk>/', PostUpdateView.as_view(), name='post_edit'),
    path('search/', Search.as_view(), name='search'),
    path('login/', PostUpdateView.as_view(template_name='users/login.html'), name='login'),
    path('category/<int:pk>', CategoryListView.as_view(), name='category'),
    path('cat_detail/<int:pk>', CategoryDetailView.as_view(), name='cat_detail'),
    path('subscribe/<int:pk>', subscribe_to_category, name='subscribe'),
    path('unsubscribe/<int:pk>/', unsubscribe_from_category, name='unsubscribe'),
]
