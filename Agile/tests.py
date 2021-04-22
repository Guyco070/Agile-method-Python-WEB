from django.test import TestCase,SimpleTestCase
from django.urls import reverse, resolve
from Agile.views import *

class Test(SimpleTestCase):

    def test_homepage_url(self):
        response = self.client.get('')
        self.assertEquals(response.status_code, 200)

    def test_SIGNUP_url(self):
        response = self.client.get('/SIGNUP')
        self.assertEquals(response.status_code, 200)

    def test_LOGIN_url(self):
        response = self.client.get('/LOGIN')
        self.assertEquals(response.status_code, 200)

    def test_SignUpDone_url(self):
        response = self.client.get('/SignUpDone')
        self.assertEquals(response.status_code, 200)

