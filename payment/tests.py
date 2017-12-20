from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from management.commands.access_control import Command

# Create your tests here.

class SubscriptionTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username = "zabid",
            first_name = "Zeeshan",
            last_name = "Abid",
            password="password"
        )

        user.save()


        user = User.objects.create_user(
            username = "Michael",
            first_name = "Michael",
            last_name = "Russo",
            password = "password"
        )

        user.save()

        command = Command()
        command.handle()



    def test_subscriptions_create_post_request(self):
        client = Client()
        client.login(username = "zabid", password = "password")

        post_request = {
            'operation':'create',
            'plan_name':'MONTHLY',
            'nonce':'fake-valid-nonce'
        }

        response = client.post("/payment/subscribe/", data = post_request)


        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)

    def test_subscriptions_delete_post_request(self):
        client = Client()
        client.login(username = "zabid", password = "password")

        post_request = {
            'operation':'delete',
            'plan_name':'MONTHLY'
        }

        response = client.post("/payment/subscribe/", data = post_request)

        self.assertEqual(response.status_code, 200)



    def test_get_payment_page(self):
       pass