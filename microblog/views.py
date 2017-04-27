from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post


class PublishedPostsMixin(object):

    def get_queryset(self):
        return self.model.objects.live()


class PostListView(LoginRequiredMixin, PublishedPostsMixin, ListView):
    model = Post


class PostDetailView(LoginRequiredMixin, PublishedPostsMixin, DetailView):
    model = Post
