from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
import time

from django.contrib.auth import (
    get_user_model,
)
from faker import Faker

User = get_user_model()


class MessageApiTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('messages')
        self.faker_obj = Faker()

        self.user = self.setup_user()
        self.token = Token.objects.get(user=self.user)

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_message_api_unauthorized_request(self):
        message_data = {
            'message': 'hasib',
        }
        response = self.client.post(self.url, message_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_message_api_authorized_request(self):
        message_data = {
            'message': 'hasib',
        }

        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token.key)}
        response = self.client.post(self.url, data=message_data, **header)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_less_then_10_msg_in_one_hour_success(self):
        message_data = {
            'message': 'hasib',
        }

        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token.key)}
        for _ in range(10):
            response = self.client.post(self.url, data=message_data, **header)            
            self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_10_msg_in_one_hour_success(self):
        message_data = {
            'message': 'hasib',
        }

        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token.key)}
        for _ in range(11):
            response = self.client.post(self.url, data=message_data, **header)            
            self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_more_than_10_msg_in_one_hour_filure(self):
        message_data = {
            'message': 'hasib',
        }

        header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token.key)}
        for count in range(12):
            response = self.client.post(self.url, data=message_data, **header)            
            # why need sleep? race condition??
            time.sleep(1) # .500
            if count == 11:
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
                self.assertEqual(response.data.get('error'), '1 hour Msg Quota Complete')

