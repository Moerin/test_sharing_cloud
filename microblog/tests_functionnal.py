import os
from selenium import webdriver
from django.conf import settings

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import activate
from django.contrib.staticfiles.testing import LiveServerTestCase

from .forms import PostForm


class LiveServerMixin(object):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        return super(LiveServerMixin, self).setUp()

    def tearDown(self):
        self.browser.quit()
        return super(LiveServerMixin, self).tearDown()

    def get_full_url(self, namespace):
        return self.live_server_url + reverse(namespace)


class HomeNewVisitorTest(LiveServerMixin, LiveServerTestCase):

    def test_home_title(self):
        self.browser.get(self.get_full_url("microblog:list"))
        self.assertIn("Sharing Blog", self.browser.title)

    def test_h1_css(self):
        self.browser.get(self.get_full_url("microblog:list"))
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(h1.value_of_css_property("color"),
                         "rgb(51, 51, 51)")


class TranslationTests(LiveServerMixin, LiveServerTestCase):

    def test_internationalization_en(self):
        lang, a_text = ('en', 'Login with Google')
        activate(lang)
        self.browser.get(self.get_full_url("microblog:list"))
        a = self.browser.find_element_by_tag_name("a")
        self.assertEqual(a.text, a_text)

    def test_internationalization_fr(self):
        lang, a_text = ('fr', 'Connection via Google')
        import ipdb; ipdb.set_trace()  # XXX BREAKPOINT

        activate(lang)
        self.browser.get(self.get_full_url("microblog:list"))
        a = self.browser.find_element_by_tag_name("a")
        self.assertEqual(a.text, a_text)


class AppFormTests(TestCase):

    def test_form_is_valid(self):
        form_data = {'title': 'TOTO', 'content': 'Pouet'}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_not_valid(self):
        form_data = {'title': 'TOTO'}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())


class PostTests(TestCase):

    def test_redirect_to_login(self):
        response = self.client.get(reverse('microblog:list'))

        assert response.status_code == 302
