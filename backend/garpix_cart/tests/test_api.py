from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from garpix_user.models import UserSession

from rest_framework.test import APIClient

from ..models import CartItem


class CartViewTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.username = 'testuser1'
        self.password = '12345'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.customer = UserSession.objects.create(user=self.user, recognized=UserSession.UserState.REGISTERED)
        self.user.save()
        client = APIClient()
        client.force_authenticate(user=self.user)
        self.client = client

    def test_add(self):
        response = self.client.post(
            reverse('garpix_cart:cart-add'),
            {
                'data': [
                    {
                        'product': 1,
                        'count': 1,
                        'params': {
                            'color': '#000000'
                        }
                    }
                ]
            },
            format='json',
            HTTP_ACCEPT='application/json'
        )

        self.assertEqual(response.status_code, 200)
        count = CartItem.objects.all().count()
        self.assertEqual(count, 1)

    def test_session_add(self):
        response = self.client.post(
            reverse('garpix_cart:cart-session-add'),
            {
                'data': [
                    {
                        'product': 1,
                        'count': 1,
                        'params': {
                            'color': '#000000'
                        }
                    }
                ]
            },
            format='json',
            HTTP_ACCEPT='application/json'
        )

        self.assertEqual(response.status_code, 200)
        count = CartItem.objects.all().count()
        self.assertEqual(count, 1)

    def test_remove(self):
        cart_item = CartItem(
            product=1,
            count=1,
            params=dict(),
            customer=self.customer
        )
        cart_item.save()

        response = self.client.delete(
            reverse('garpix_cart:cart-remove'),
            {
                'data': [
                    cart_item.pk
                ]
            },
            format='json',
            HTTP_ACCEPT='application/json'
        )

        self.assertEqual(response.status_code, 200)

        count = CartItem.objects.all().count()
        self.assertEqual(count, 0)

    def test_session_remove(self):
        cart_item = CartItem(
            product=1,
            count=1,
            params=dict(),
            customer=self.customer
        )
        cart_item.save()

        response = self.client.delete(
            reverse('garpix_cart:cart-session-remove'),
            {
                'data': [
                    cart_item.pk
                ]
            },
            format='json',
            HTTP_ACCEPT='application/json'
        )

        self.assertEqual(response.status_code, 200)

        count = CartItem.objects.all().count()
        self.assertEqual(count, 0)

    def test_update(self):
        product_count = 2
        cart_item = CartItem(
            product=1,
            count=1,
            params=dict(),
            customer=self.customer
        )
        cart_item.save()

        response = self.client.patch(
            reverse('garpix_cart:cart-detail', args=[cart_item.pk]),
            {
                'data': {
                    'count': product_count
                }
            },
            format='json',
            HTTP_ACCEPT='application/json'
        )

        self.assertEqual(response.status_code, 200)

        obj = CartItem.objects.get(pk=cart_item.pk)
        self.assertEqual(obj.count, product_count)

    def test_get_list_cart(self):
        CartItem.objects.create(customer=self.customer, count=1, params={}, product=10)
        response = self.client.get(
            reverse('garpix_cart:cart-list'),
            format='json',
            HTTP_ACCEPT='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
