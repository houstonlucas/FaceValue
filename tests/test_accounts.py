from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsTests(TestCase):
    def test_signup_page_status_code(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page_content(self):
        response = self.client.get(reverse('signup'))
        self.assertContains(response, "Sign Up")

    def test_signup_form(self):
        signup_url = reverse('signup')
        data = {
            'username': 'testuser',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123',
        }
        response = self.client.post(signup_url, data)
        # After successful signup, should redirect to home
        self.assertRedirects(response, reverse('home'))
        # User should be created and authenticated
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)
        # Check session has user id
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_page_status_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_form(self):
        # Create a user to log in
        User.objects.create_user(username='loginuser', password='TestPass123')
        login_url = reverse('login')
        data = {
            'username': 'loginuser',
            'password': 'TestPass123',
        }
        response = self.client.post(login_url, data)
        # After login, should redirect to home
        self.assertRedirects(response, reverse('home'))
        # Check session has user id
        self.assertTrue('_auth_user_id' in self.client.session)
