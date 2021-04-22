from django.test import TestCase,SimpleTestCase
from django.urls import reverse, resolve
from Agile.views import *

class Test(SimpleTestCase):

    def test_homepage_url(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

