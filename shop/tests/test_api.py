from rest_framework.test import APITestCase
from django.urls import reverse
from shop.models import Gadget
from shop.serializers import GadgetSerializer
from rest_framework import status


class GadgetApiTestCase(APITestCase):
    def test_get_obj(self):
        phone_1 = Gadget.objects.create(name='Iphone', description='Good', price=150000, exist='1')

        response = self.client.get(reverse('gadget_api_detail', args=[1]))
        print(response)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(phone_1.name, response.data['name'])