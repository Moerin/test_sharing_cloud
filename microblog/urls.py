from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import PostListView
from .views import PostDetailView

urlpatterns = [
    url(r'^$', PostListView.as_view(), name='list'),
    url(r'^blog/$', PostListView.as_view(), name='list'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^blog/(?P<slug>[\w-]+)/$', PostDetailView.as_view(), name='detail'),
]
