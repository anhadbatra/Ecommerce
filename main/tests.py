from django.test import TestCase,Client,override_settings
from django.urls import reverse
from .models import User
from unittest.mock import patch

class UserRegister_Test(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')
    def test_register_page_load(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'login_register/register.html')
    @override_settings(RECAPTCHA_ENABLED=True)
    @patch('main.views.requests.post') 
    def test_user_Register(self,mock_post):
        mock_post.return_value.json.return_value = {'success': True}
        data = {
            'first_name' : 'Test',
            'last_name' : 'Test',
            'emailid':'test123@gmail.com',
            'password' : 'StrongPass123',
            'g-recaptcha-response': 'dummy-token'

        }
        response = self.client.post(self.url,data)
        if response.status_code == 200 and 'form' in response.context:
            print("Form errors:", response.context['form'].errors)
        self.assertEqual(response.status_code,200)
        self.assertTrue(User.objects.filter(email='test123@gmail.com').exists())


