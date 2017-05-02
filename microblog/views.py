import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.views.generic.edit import FormMixin
from tornado_websockets.websocket import WebSocket

from .forms import PostForm
from .models import Post


# Websockets initialization
tws, dws = WebSocket('/messages'), WebSocket('/deletes')


class GetUniquePostMixin(object):
    """Mixin to get unique model by constraint (slug, author)"""

    def get_object(self):
        return Post.objects.get(slug=self.kwargs['slug'], author=self.request.user)


class CheckUserOwnerMixin(object):
    """Mixin to check if action (view) are authorized for the current user.
       Except for Super User.
    """

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
    """Mixin which use PostManager to get only published Post"""

    def get_queryset(self):
        return self.model.objects.live()


class PostListView(LoginRequiredMixin, PublishedPostsMixin, FormMixin, ListView):
    """View which list all Posts on index page"""

    model = Post
    form_class = PostForm


class PostDetailView(LoginRequiredMixin, PublishedPostsMixin, GetUniquePostMixin, DetailView):
    """View which will displayed detail on post, more field, delete and edit actions"""
    model = Post


class PostNewView(LoginRequiredMixin, CreateView):
    """View used to create Post and binded to WebSocket actions"""

    success_url = reverse_lazy("microblog:list")

    def __init__(self, **kwargs):
        """This method is overrided to add view instance to WebSocket context"""

        super(PostNewView, self).__init__(**kwargs)
        tws.context = self

    @tws.on
    def open(self, socket, data):
        # Notify all clients about a new connection
        tws.emit('new_connection')

    @tws.on
    def new_message(self, socket, data):
        # Notify all clients about a new messages
        tws.emit('new_message_created', data['message'])


    def post(self, request, *args, **kwargs):
        """Due to WebSocket action we need to parse the json response
           to populate the rightful fields.
        """

        post_content = self.request.POST.get('content')
        post_title = self.request.POST.get('title')
        response_data = {}

        post = Post(content=post_content,
                    title=post_title,
                    author=self.request.user)
        post.save()

        # Data for WebSocket
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
    """View which allowed edit on title and content fields"""

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


class PostDeleteView(LoginRequiredMixin, CheckUserOwnerMixin, GetUniquePostMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('microblog:list')
    template_name_suffix = '_delete'

    # Websockets purpose
    def __init__(self, **kwargs):
        """This method is overrided to add view instance to WebSocket context"""

        super(PostDeleteView, self).__init__(**kwargs)
        dws.context = self

    @dws.on
    def open(self, socket, data):
        # Notify all clients about a new connection
        dws.emit('new_connection')

    @dws.on
    def delete_action(self, socket, data):
        # Notify all clients about a new messages
        dws.emit('delete_action_made', data['message'])

    def post(self, request, *args, **kwargs):
        """DeleteView is used by Regular form in login_detail and
           by ajax request.
           Process workflow need to be identified and managed.
        """

        if self.request.is_ajax():
            slug = kwargs['slug']
            response_data = {}

            post = Post.objects.get(slug=slug,
                                    author=self.request.user)
            post.delete()

            response_data['result'] = 'Delete post successful!'

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )

        return super(DeleteView, self).post(request, *args, **kwargs)
