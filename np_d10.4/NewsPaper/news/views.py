from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.core.paginator import Paginator
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.urls import resolve

from django.http.response import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.core.cache import cache

# from NewsPaper.settings import DEFAULT_FROM_EMAIL
from django.conf import settings

DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL


class News(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-dateCreation']
    form_class = PostForm
    paginate_by = 8  # постраничный вывод в 1элемент

    def get_queryset(self):
        queryset = PostFilter(self.request.GET, super().get_queryset()).qs
        # фильтрация queryset-ом
        return queryset

    def get_context_data(self, **kwargs):  # забираем отфильтрованные
        # объекты переопределяя метод get_context_data у
        # наследуемого класса - полиморфизм
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        # context['form'] = PostForm()
        return context

    # def post(self, request, *args, **kwargs):
    #     # берём значения для нового товара из POST-запроса отправленного на сервер
    #     form = self.form_class(request.POST)
    #
    #     if form.is_valid():
    #         form.save()
    #     return super().get(request, *args, **kwargs)


# создаём представление, в котором будут детали конкретного отдельного товара
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'news/post_detail.html'  # название шаблона будет product.html
    queryset = Post.objects.all()
    context_object_name = 'post'  # название объекта

    def post_list_view(request):
        paginator = Paginator(News.objects.all(), per_page=7)
        page = paginator.page(request.GET.get('page', 2))
        return render(request, 'news/news.html', {
            'object_list': page.object_list,
            'page_obj': page,
        })

    def get_object(self, *args, **kwargs):  # переопределим метод получения объекта
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        # кэш очень похож на словарь, и метод get действует
        # также. Он забирает значение по ключу - если его
        # нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


#  ++ дженерик для создания объекта. Надо указать только имя шаблона и класс формы
#  который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news/post_create.html'
    form_class = PostForm
    context_object_name = 'news'
    permission_required = ('news.add_post',)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        user = request.user
        if form.is_valid():
            post = form.save(commit=False)
            # post.authorUser = Author.objects.get_or_create(user=user)[0]
            return self.form_valid(form)
        return redirect('news')


# дженерик для редактирования объекта
class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'news/post_edit.html'
    form_class = PostForm
    context_object_name = 'news'
    permission_required = ('news.change_post',)

    # метод get_object вместо queryset для получения инфо об obj редактирования
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news'
    permission_required = ('news.delete_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class Search(ListView):  # дженерик для поиска поста
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты,
    # его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    ordering = ['-dateCreation']  # сортировка по дате публикации, сначала более новые  или
        # queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 8

    def get_queryset(self):
        queryset = PostFilter(self.request.GET, super().get_queryset()).qs  # фильтрация queryset-ом
        return queryset

    def get_context_data(self, **kwargs):
        # забираем отфильтрованные объекты переопределяя метод get_context_data у
        # наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        # вписываем наш фильтр в контекст
        context['form'] = PostForm()
        return context


class CategoryListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/cat.html'
    context_object_name = 'news'  # коллекция записей из БД
    ordering = ['-dateCreation']
    paginate_by = 3

    def get_queryset(self):
        self.id = resolve(self.request.path_info).kwargs['pk']
        c = Category.objects.get(id=self.id)
        queryset = Post.objects.filter(postCategory=c)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = Category.objects.get(id=self.id)
        context['cat'] = Category.objects.get(pk=self.kwargs['pk'])
        context['subscribers'] = category.subscribers.all()
        subscribed = category.subscribers.filter(email=user.email)
        # if not subscribed:
        #     context['sub'] = True
        # else:
        #     context['sub'] = False
        context['category'] = category
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'news/cat_detail.html'
    queryset = Category.objects.all()
    context_object_name = 'categorys'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_object_name = 'category'
        user = self.request.user
        cat = Category.objects.values('name')
        context['category_list'] = Category.objects.get(pk=self.kwargs['pk'])

    def show_category(request, category_id):
        return HttpResponse(f"Отображение категории с id = {category_id}")


@login_required
def subscribe_to_category(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribers.add(request.user.id)
    return redirect(request.META.get('HTTP_REFERER'))  # возвращает на страницу, с кот-й поступил запрос


@login_required
def unsubscribe_from_category(request, pk):  # отписаться от категории
    category = Category.objects.get(pk=pk)
    category.subscribers.remove(request.user.id)
    return redirect(request.META.get('HTTP_REFERER'))
