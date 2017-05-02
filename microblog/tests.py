import os
from django.conf import settings

from django.core.urlresolvers import reverse
from django.test import TestCase

from .forms import PostForm


class AppFormTests(TestCase):

    def test_form_is_valid(self):
        form_data = {'title': 'TOTO', 'content': 'Pouet'}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_not_valid(self):
        form_data = {'title': 'TOTO'}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())


class PostTestCase(TestCase):

    def test_redirect_to_login(self):
        response = self.client.get(reverse('microblog:list'))

        assert response.status_code == 302
