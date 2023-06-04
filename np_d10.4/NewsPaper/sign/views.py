from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.views.generic.edit import CreateView
from .models import BaseRegisterForm

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'
#  файле представлений реализуем Create-дженерик.
# * модель формы, которую реализует данный дженерик;
# * форма, которая будет заполняться пользователем;
# * URL, на который нужно направить пользователя
# после успешного ввода данных в форму.
# Также мы должны модифицировать файл конфигурации URL,
# чтобы Django мог увидеть это представление.


@login_required  # view для апгрейда аккаунта до Premium, т.е добавление
# в группу premium.
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')  # - перенаправляем пользователя на корневую стр.
    # В этом листинге кода мы получили объект текущего пользователя
    # из переменной запроса. Вытащили premium-группу из модели Group.
    # - проверяем, находится ли пользователь в этой группе (вдруг
    # кто-то решил перейти по этому URL, уже имея Premium). И если он
    # всё-таки ещё не в ней — смело добавляем.
