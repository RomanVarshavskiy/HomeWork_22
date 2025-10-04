"""Представления (Class-Based Views) для приложения блога.

Содержит CRUD-представления для модели BlogPost, а также логику инкремента счётчика
просмотров и отправки уведомления при достижении порога просмотров.
"""


from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from django.core.mail import send_mail

from myblog.models import BlogPost


class BlogPostCreateView(CreateView):
    """Создание публикации блога.

    Атрибуты:
        model: Модель публикации.
        fields: Поля, доступные для ввода в форме.
        template_name: Шаблон формы создания записи.
        success_url: URL для редиректа после успешного создания.
    """

    model = BlogPost
    fields = ['title', 'content', 'preview_image', 'created_at', 'updated_at', 'is_published', 'views_counter']
    template_name = 'myblog/blogpost_form.html'
    success_url = reverse_lazy('myblog:blogposts_list')


class BlogPostListView(ListView):
    """Список опубликованных публикаций блога.

    Атрибуты:
      model: Модель публикации.
      template_name: Шаблон списка.
      context_object_name: Имя переменной контекста со списком публикаций.
    """

    model = BlogPost
    template_name = 'myblog/blogposts_list.html'
    context_object_name = 'blogposts'

    def get_queryset(self):
        """Возвращает QuerySet только опубликованных записей.

        Возврат:
            QuerySet[BlogPost]: отфильтрованные записи с is_published=True.
        """
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """Детальная страница публикации.

    Дополнительно:
        - Увеличивает счётчик просмотров при каждом обращении.
        - Отправляет уведомление по email при достижении заданного порога просмотров.
    """

    model = BlogPost
    template_name = 'myblog/blogpost_detail.html'
    context_object_name = 'blogpost'

    def get_object(self, queryset=None):
        """Возвращает объект публикации и применяет побочные эффекты.

        Побочные эффекты:
            - Инкрементирует поле views_counter и сохраняет модель.
            - При достижении 100 просмотров отправляет письмо через send_mail().

        Параметры:
            queryset: Необязательный QuerySet для выборки объекта.

        Возврат:
            BlogPost: актуальный объект публикации с обновлённым счётчиком.
        """
        obj = super().get_object(queryset)
        obj.views_counter += 1
        obj.save()
        obj.refresh_from_db(fields=['views_counter'])
        if obj.views_counter == 100:
            send_mail(
                subject='Поздравляем! 100 просмотров статьи',
                message=f'Статья "{obj.title}" набрала 100 просмотров.',
                from_email=None,
                recipient_list=['recipient@exemple.com'],
                fail_silently=False,
            )
        return obj


class BlogPostUpdateView(UpdateView):
    """Редактирование публикации блога.

    Атрибуты:
        model: Модель публикации.
        fields: Поля, доступные для редактирования.
        template_name: Шаблон формы редактирования.
        success_url: URL по умолчанию для редиректа (может быть перекрыт get_success_url()).
    """

    model = BlogPost
    fields = ['title', 'content', 'preview_image', 'created_at', 'updated_at', 'is_published', 'views_counter']
    template_name = 'myblog/blogpost_form.html'
    success_url = reverse_lazy('myblog:blogposts_list')

    def get_success_url(self):
        """Возвращает URL для редиректа после успешного обновления.
        Ведёт на детальную страницу отредактированной публикации.
        """
        return reverse('myblog:blogpost_detail', args={self.kwargs.get('pk')})


class BlogPostDeleteView(DeleteView):
    """Удаление публикации блога.

    Атрибуты:
        model: Модель публикации.
        template_name: Шаблон подтверждения удаления.
        success_url: URL для редиректа после успешного удаления (к списку публикаций).
    """
    model = BlogPost
    template_name = 'myblog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('myblog:blogposts_list')
