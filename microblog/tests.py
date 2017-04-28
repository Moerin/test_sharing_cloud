from django.core.urlresolvers import reverse
from django.test import TestCase


class PostTestCase(TestCase):

    def setUp(self):
        pass

    def test_redirect_to_login(self):
        response = self.client.get(reverse('microblog:list'))

        assert response.status_code == 302
