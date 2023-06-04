from django_filters import FilterSet, ModelChoiceFilter  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post, Category


# создаём фильтр
class PostFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля,
    # по которым будет фильтроваться (т.е. подбираться) информация о товарах
    category = ModelChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label='Тематика',
        empty_label='не выбрано'
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],  # хотя бы отдалённо похожее запрашиваем
            'dateCreation': ['gt'],  # дата больше или равна запрошенной
            'text': ['icontains'],
            'author': ['exact'],  # фильтр по автору
            'categoryType': ['exact'],
            # 'postCategory': ['exact'],
        }
