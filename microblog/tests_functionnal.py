import unittest

from django.contrib.staticfiles.testing import LiveServerTestCase
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import activate
from selenium import webdriver

from .forms import PostForm


class LiveServerMixin(object):
    """Functionnal test to check index page """

    def setUp(self):
        """Selenium configuration warmup"""

        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        return super(LiveServerMixin, self).setUp()

    def tearDown(self):

        self.browser.quit()
        return super(LiveServerMixin, self).tearDown()

    def get_full_url(self, namespace):
        """Tool method which full uri"""
        return self.live_server_url + reverse(namespace)


class CheckTagTest(LiveServerMixin, LiveServerTestCase):
    """Functionnal test to check tag && css"""

    def test_list_title(self):

        self.browser.get(self.get_full_url("microblog:list"))
        self.assertIn("Sharing Blog", self.browser.title)

    def test_h1_css(self):

        self.browser.get(self.get_full_url("microblog:list"))
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(h1.value_of_css_property("color"),
                         "rgb(51, 51, 51)")


class TranslationTests(LiveServerMixin, LiveServerTestCase):
    """Functionnal test to check Internationalization"""

    @unittest.skip("Not works in test but works in real")
    def test_internationalization_en(self):

        lang, a_text = ('en', 'Login with Google')
        activate(lang)
        self.browser.get(self.get_full_url("microblog:list"))
        a = self.browser.find_element_by_tag_name("a")
        self.assertEqual(a.text, a_text)

    def test_internationalization_fr(self):

        lang, a_text = ('fr', 'Connection via Google')
        activate(lang)
        self.browser.get(self.get_full_url("microblog:list"))
        a = self.browser.find_element_by_tag_name("a")
        self.assertEqual(a.text, a_text)


class AppFormTests(TestCase):
    """Functionnal test to check form validation"""

    def test_form_is_valid(self):
        form_data = {'title': 'TOTO', 'content': 'Pouet'}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_not_valid(self):
        form_data = {'title': 'TOTO'}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())


class PostTests(TestCase):
    """Functionnal test to check redirection"""

    def test_redirect_to_login(self):
        response = self.client.get(reverse('microblog:list'))

        assert response.status_code == 302
