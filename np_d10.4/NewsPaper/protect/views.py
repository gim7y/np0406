from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'  # создали
    # generic-представление для отображения шаблона, унаследовав
    # кастомный класс-представление от TemplateView и указав имя
    # шаблона + унаследовали это представление от миксина
    # проверки аутентификации.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context
