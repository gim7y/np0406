from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    # переопределяем метод ready, чтобы при готовности приложения
    # импортировался модуль со всеми функциями обработчиками
    def ready(self):
        import news.signals
