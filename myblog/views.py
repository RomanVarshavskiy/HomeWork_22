from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from myblog.models import BlogPost


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content', 'preview_image', 'created_at', 'updated_at', 'is_published',  'views']
    template_name = 'myblog/blogpost_form.html'
    success_url = reverse_lazy('myblog:blogposts_list')


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'myblog/blogposts_list.html'
    context_object_name = 'blogposts'


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'myblog/blogpost_detail.html'
    context_object_name = 'blogpost'


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'preview_image', 'created_at', 'updated_at', 'is_published', 'views']
    template_name = 'myblog/blogpost_form.html'
    success_url = reverse_lazy('myblog:blogposts_list')


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'myblog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('myblog:blogposts_list')
