from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post
from .forms import PostForm


class PublishedPostsMixin(object):

    def get_queryset(self):
        return self.model.objects.live()


class PostListView(LoginRequiredMixin, PublishedPostsMixin, ListView):
    model = Post


class PostDetailView(LoginRequiredMixin, PublishedPostsMixin, DetailView):
    model = Post


class PostNewView(LoginRequiredMixin, FormView):
    template_name = 'microblog/post_new.html'
    form_class = PostForm
    success_url = '/'

    def form_valid(self, form):

        if form.is_valid():
            post = form.save(commit=False)
            post.author = self.request.user
            post.save()

        return super(PostNewView, self).form_valid(form)
