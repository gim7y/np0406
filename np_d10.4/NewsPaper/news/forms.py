from django import forms
from django.forms import ModelForm, BooleanField, Textarea  # Импортируем true-false поле
from django_filters import ModelChoiceFilter

from .models import Post, PostCategory, Category


# Создаём модельную форму
class PostForm(ModelForm):
    check_box = BooleanField(label='Галочка!')  # добавляем галочку или же true-false поле

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['author.authorUser|title'].empty_label = "Автор не выбран"
        self.fields[''].empty_label = "Не выбрано"
    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля.
    # Мы уже делали что-то похожее с фильтрами.


    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'categoryType', 'postCategory', 'check_box']
        widgets = {
            'text': forms.Textarea(attrs={'cols': 50, 'rows': 2}),
        }
