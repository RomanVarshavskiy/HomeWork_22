"""Представления (Class-Based Views) для приложения блога.

Содержит CRUD-представления для модели BlogPost, а также логику инкремента счётчика
просмотров и отправки уведомления при достижении порога просмотров.
"""
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from myblog.forms import BlogPostForm, BlogPostModeratorForm
from myblog.models import BlogPost
from myblog.services import get_blogpost_from_cache


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    """Создание публикации блога.

    Атрибуты:
        model: Модель публикации.
        fields: Поля, доступные для ввода в форме.
        template_name: Шаблон формы создания записи.
        success_url: URL для редиректа после успешного создания.
    """

    model = BlogPost
    form_class = BlogPostForm
    template_name = "myblog/blogpost_form.html"
    success_url = reverse_lazy("myblog:blogposts_list")


    def form_valid(self, form):
        """Автопривязка владельца к текущему пользователю."""
        blogpost = form.save(commit=False)
        blogpost.author = self.request.user
        blogpost.save()
        return super().form_valid(form)


class BlogPostListView(ListView):
    """Список опубликованных публикаций блога.

    Атрибуты:
      model: Модель публикации.
      template_name: Шаблон списка.
      context_object_name: Имя переменной контекста со списком публикаций.
    """

    model = BlogPost
    template_name = "myblog/blogposts_list.html"
    context_object_name = "blogposts"

    def get_queryset(self):
        """Возвращает QuerySet из кэша."""
        return get_blogpost_from_cache


class BlogPostDetailView(LoginRequiredMixin, DetailView):
    """Детальная страница публикации.

    Дополнительно:
        - Увеличивает счётчик просмотров при каждом обращении.
        - Отправляет уведомление по email при достижении заданного порога просмотров.
    """

    model = BlogPost
    template_name = "myblog/blogpost_detail.html"
    context_object_name = "blogpost"

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
        obj.refresh_from_db(fields=["views_counter"])
        if obj.views_counter == 100:
            send_mail(
                subject="Поздравляем! 100 просмотров статьи",
                message=f'Статья "{obj.title}" набрала 100 просмотров.',
                from_email=None,
                recipient_list=["recipient@exemple.com"],
                fail_silently=False,
            )
        return obj


class BlogPostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование публикации блога.

    Атрибуты:
        model: Модель публикации.
        fields: Поля, доступные для редактирования.
        template_name: Шаблон формы редактирования.
        success_url: URL по умолчанию для редиректа (может быть перекрыт get_success_url()).
    """

    model = BlogPost
    form_class = BlogPostForm
    template_name = "myblog/blogpost_form.html"
    success_url = reverse_lazy("myblog:blogpost_detail")
    permission_required = "myblog.change_blogpost"
    raise_exception = True

    def has_permission(self):
        """Разрешаем редактирование только владельцу, суперпользователю или модератору."""
        user = self.request.user
        obj = self.get_object()
        if user.is_superuser:
            return True
        # модератор, который может только менять публикацию
        if user.has_perm("myblog.change_blogpost"):
            return True
        # владелец объекта
        return obj.author_id == user.id

    def get_queryset(self):
        """Ограничим базовый queryset владельцем для безопасности (кроме суперпользователя/модератора)."""
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser or user.has_perm("myblog.change_blogpost"):
            return qs
        return qs.filter(author=user)

    def get_success_url(self):
        """URL для редиректа после успешного обновления.
        Ведёт на страницу детали товара.
        """
        return reverse_lazy("myblog:blogpost_detail", args=[self.kwargs.get("pk")])

    def get_form_class(self):
        user = self.request.user
        if user.is_superuser:
            return BlogPostForm
        if user.has_perm("myblog.change_blogpost"):
            return BlogPostModeratorForm
        # владелец может редактировать полную форму
        obj = self.get_object()
        if obj.author_id == user.id:
            return BlogPostForm
        raise PermissionDenied


class BlogPostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление публикации блога.

    Атрибуты:
        model: Модель публикации.
        template_name: Шаблон подтверждения удаления.
        success_url: URL для редиректа после успешного удаления (к списку публикаций).
    """

    model = BlogPost
    template_name = "myblog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("myblog:blogposts_list")
    permission_required = "myblog.delete_blogpost"
    raise_exception = True

    def has_permission(self):
        """Удалять может только владелец или суперпользователь или модератор."""
        user = self.request.user
        obj = self.get_object()
        if user.is_superuser:
            return True
        # модератор
        if user.has_perm("myblog.delete_blogpost"):
            return True
        # владелец объекта
        return obj.author_id == user.id

    def get_queryset(self):
        """Ограничим удаление только своих объектов (кроме суперпользователя)."""
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser or user.has_perm("myblog.delete_blogpost"):
            return qs
        return qs.filter(author=user)
