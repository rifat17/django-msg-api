from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


from django.contrib.auth import (
    get_user_model,
)
from faker import Faker

User = get_user_model()

def register(client, url, **kwargs):
    return client.post(url, kwargs)


class UserAuthTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')
        self.faker_obj = Faker()
        self.register_data = {
            'username': 'hasib',
            'password': 'testpass1',
            'confirm_password': 'testpass1',
            'email': 'email@mail.com',
        }

    def test_if_data_is_correct_then_register(self):
        
        # response = self.client.post(self.url, register_data)
        response = register(self.client, self.url, **self.register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_if_username_is_incorrect_not_register(self):
        register_data = {
            'username': '',
            'password': 'testpass1',
            'confirm_password': 'testpass1',
            'email': 'email@mail.com',
        }
        response = self.client.post(self.url, register_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_password_is_incorrect_not_register(self):
        register_data = {
            'username': 'hasib',
            'password': 'testpass1',
            'confirm_password': 'testpass',
            'email': 'email@mail.com',
        }
        response = self.client.post(self.url, register_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

"""     def test_login(self):
        reg = register(self.client, self.url, )
        # login = self.client.post(reverse('login'), {'username': self.register_data.get('username'),'password': self.register_data.get('password')})
        # response = self.client.login(username=self.register_data.get('username'), password=self.register_data.get('password'))
        response = self.client.login(username=self.register_data.get('username'), password=self.register_data.get('password'))
        print(response)
        # self.assertEqual(login.status_code, status.HTTP_200_OK)
 """


