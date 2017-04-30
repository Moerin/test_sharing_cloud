import json

from tornado_websockets.websocket import WebSocket

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.views.generic.edit import FormMixin

from .forms import PostForm
from .models import Post

tws = WebSocket('/messages')


class CheckUserOwnerMixin(object):

    def dispatch(self, request, *args, **kwargs):
        # check for user permission:
        # Take pk from kwargs
        slug = kwargs.get('slug')  # example
        # Take user from request
        author = request.user
        # If super user we get all access
        if request.user.is_superuser:
            try:
                Post.objects.get(slug=slug)
                return super(CheckUserOwnerMixin, self).dispatch(request, *args, **kwargs)
            except Post.DoesNotExist, e:
                return HttpResponseNotFound("No post with the following slug %s" % slug)

        # check permission
        try:
            Post.objects.get(slug=slug, author=author)
            return super(CheckUserOwnerMixin, self).dispatch(request, *args, **kwargs)
        except Post.DoesNotExist, e:
            return HttpResponseForbidden("You are not the owner of this message you can't delete it")


class PublishedPostsMixin(object):

    def get_queryset(self):
        return self.model.objects.live()


class PostListView(LoginRequiredMixin, PublishedPostsMixin, FormMixin, ListView):
    model = Post
    form_class = PostForm


class PostDetailView(LoginRequiredMixin, PublishedPostsMixin, DetailView):
    model = Post


class PostNewView(LoginRequiredMixin, CreateView):
    success_url = reverse_lazy("microblog:list")
    messages = list()

    # Websockets purpose
    def __init__(self, **kwargs):
        super(PostNewView, self).__init__(**kwargs)

        print "avant"
        print tws.context
        tws.context = self
        print "apres"
        print tws.context


    @tws.on
    def connection(self, socket, data):
        import ipdb; ipdb.set_trace()  # XXX BREAKPOINT

        # Send an history of the chat
        [socket.emit('new_message', __) for __ in self.messages]
        tws.emit('new_connection', '%s just joined the webchat.' % data.get('username', '<Anonymous>'))

    @tws.on
    def message(self, socket, data):
        message = {
            'username': data.get('username', '<Anonymous>'),
            'message': data.get('message', 'Empty message')
        }

        tws.emit('new_message', message)
        self.messages.append(message)

    @tws.on
    def clear_history(self, socket, data):
        """
            Called when a client wants to clear messages history.
            Used only for client-side JavaScript unit tests
        """

        self.messages = []

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
        response_data['slug'] = post.slug
        response_data['content'] = post.content
        response_data['created'] = post.created_at.strftime('%B %d, %Y %I:%M %p')
        response_data['username'] = post.author.username

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
