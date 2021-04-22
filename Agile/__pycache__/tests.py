from django.test import TestCase,SimpleTestCase
from django.urls import reverse, resolve
from Agile.views import *

class Test(SimpleTestCase):

    def test_homepage_url(self):
        url = reverse('homepage')
        self.assertEquals(resolve(url),func,HomePage)

