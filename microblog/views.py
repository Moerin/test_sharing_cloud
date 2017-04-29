import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.views.generic.edit import FormMixin

from .forms import PostForm
from .models import Post


class CheckUserOwnerMixin(object):

    def dispatch(self, request, *args, **kwargs):
        # check for user permission:
        # Take pk from kwargs
        slug = kwargs.get('slug')  # example
        # Take user from request
        author = request.user
        # check permission
        try:
            Post.objects.get(slug=slug, author=author)
            return super(CheckUserOwnerMixin, self).dispatch(request, *args, **kwargs)
        except Post.DoesNotExist, e:
            return HttpResponseForbidden()


class PublishedPostsMixin(object):

    def get_queryset(self):
        return self.model.objects.live()


class PostListView(LoginRequiredMixin, PublishedPostsMixin, FormMixin, ListView):
    model = Post
    form_class = PostForm


class PostDetailView(LoginRequiredMixin, PublishedPostsMixin, DetailView):
    model = Post


class PostNewView(LoginRequiredMixin, CreateView):
    # template_name = 'microblog/post_new.html'
    # form_class = PostForm
    success_url = reverse_lazy("microblog:list")

    def post(self, request, *args, **kwargs):

        post_content = self.request.POST.get('content')
        post_title = self.request.POST.get('title')
        response_data = {}

        post = Post(content=post_content,
                    title=post_title,
                    author=self.request.user)
        post.save()

        response_data['result'] = 'Create post successful!'
        response_data['post_id'] = post.id
        response_data['title'] = post.title
        response_data['content'] = post.content
        response_data['created'] = post.created_at.strftime('%B %d, %Y %I:%M %p')
        response_data['author'] = post.author.username

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


class PostEditView(LoginRequiredMixin, CheckUserOwnerMixin, UpdateView):
    model = Post
    template_name = 'microblog/post_new.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse('microblog:detail', kwargs={'slug': self.slug})

    def form_valid(self, form):

        if form.is_valid():
            post = form.save(commit=False)
            post.author = self.request.user
            post.save()
            self.slug = post.slug

        return super(PostEditView, self).form_valid(form)


class PostDeleteView(LoginRequiredMixin, CheckUserOwnerMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('microblog:list')
    template_name_suffix = '_delete'
