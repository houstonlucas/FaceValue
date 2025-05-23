from django.test import SimpleTestCase
from django.urls import reverse


class HomePageTests(SimpleTestCase):
    def test_homepage_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_content(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Face Value")
        self.assertContains(response, "site is up and running")