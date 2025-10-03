from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from django.core.mail import send_mail
from django.db.models import F

from myblog.models import BlogPost


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content', 'preview_image', 'created_at', 'updated_at', 'is_published', 'views_counter']
    template_name = 'myblog/blogpost_form.html'
    success_url = reverse_lazy('myblog:blogposts_list')


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'myblog/blogposts_list.html'
    context_object_name = 'blogposts'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'myblog/blogpost_detail.html'
    context_object_name = 'blogpost'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_counter += 1
        obj.save()
        obj.refresh_from_db(fields=['views_counter'])
        if obj.views_counter == 23:
            send_mail(
                subject='Поздравляем! 23 просмотров статьи',
                message=f'Статья "{obj.title}" набрала 23 просмотров.',
                from_email=None,
                recipient_list=['recipient@exemple.com'],
                fail_silently=False,
            )
        return obj


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'preview_image', 'created_at', 'updated_at', 'is_published', 'views_counter']
    template_name = 'myblog/blogpost_form.html'
    success_url = reverse_lazy('myblog:blogposts_list')

    def get_success_url(self):
        return reverse('myblog:blogpost_detail', args={self.kwargs.get('pk')})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'myblog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('myblog:blogposts_list')
