from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, Group
import braintreeAPI
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, related_name="customer", default=None)
    braintree_id = models.CharField(max_length=50, default=None)

class Subscription(models.Model):

    class Meta:
        permissions = settings.BRAINTREE_PLANS

    PLAN_IDS = settings.BRAINTREE_PLAN_IDS

    user = models.OneToOneField(User, related_name="subscriptions", default=None)
    braintree_id = models.CharField(max_length=50, default=None)


    # Static method that takes a user (auth.models.User),plan_name (name of plan as
    # specified in braintree_plan_ids), a nonce (if customer is new),
    # plan_id (if programmer knows plan_id)
    @staticmethod
    def create_subscription(user, plan_name, nonce = None, plan_id = None, commit = True, *args, **kwargs):
        if plan_id == None:
            plan_id = settings.BRAINTREE_PLAN_IDS.get(plan_name)
            if plan_id == None:
                raise Exception("Plan Name is invalid!")

        customer = None
        if hasattr(user, "customer") == None:
            customer = braintreeAPI.braintree_get_customer(user.customer.braintree_id)
        else:
            if nonce == None:
                raise Exception("Payment Nonce is required to create a new customer")
            else:
                customer = braintreeAPI.braintree_create_customer(first_name=user.first_name,
                                                                  last_name=user.last_name,
                                                                email = user.email,
                                                                  nonce=nonce)
                newcustomer = Customer(user = user, braintree_id = customer.id)
                newcustomer.save()

        user_permissions = user.get_all_permissions()
        user_groups = user.groups.all()

        exclusive_groups = set(settings.BRAINTREE_EXCLUSIVE_GROUPS)

        new_group = None
        is_ex_group = False
        print plan_name
        try:
            new_group = Group.objects.get(name = plan_name)
        except:
            group_name = "ex_"+plan_name
            new_group = Group.objects.get(name = group_name)
            is_ex_group = True

        # if user is a member of an exclusive plan
        # or if all plans are exclusive
        # then remove all other plans
        for permission in user_permissions:
            if ((permission.find("payment.ex") > 0 and is_ex_group) or getattr(settings, 'BRAINTREE_ALL_GROUPS_EXCLUSIVE')):
                user.groups.clear()
                user.user_permissions.clear()
                user.subscription.delete()
                user.save()
                break

        payment_token = customer.payment_methods[0].token

        result = braintreeAPI.braintree_subscribe_user(payment_token, plan_id)
        if result != None:
            subscription = Subscription(user = user, braintree_id = result.id)

            if commit:
                subscription.save()

            user.groups.add(new_group)
            user.save()
            return subscription
        else:
            return None
