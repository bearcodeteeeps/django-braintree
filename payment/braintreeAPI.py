from django.conf import settings
import braintree
braintree.Configuration.configure(settings.BRAINTREE_ENVIRONMENT,
    merchant_id=settings.BRAINTREE_MERCHANT_ID,
    public_key=settings.BRAINTREE_PUBLIC_KEY,
    private_key=settings.BRAINTREE_PRIVATE_KEY)

# Creates a new braintree customer. This method is called if the
# customer is paying for the first time and needs to be created.
# NOTE: Never call this method to create a customer without
# a valid payment nonce
# Returns a braintree customer response object or False if the
# customer failed to be created.
def braintree_create_customer(first_name = None, last_name = None, email = None, nonce = None, *args, **kwargs):
        result = braintree.Customer.create({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "payment_method_nonce": nonce,
        })

        if result.is_success:
            return result.customer
        else:
            return False

# Gets a customer response object with the given ID.
# Returns a customer response object or None if the
# customer was not found.
def braintree_get_customer(id, *args, **kwargs):
    try:
        customer = braintree.Customer.find(id)
        return customer
    except braintree.NotFoundError:
        return None


# Update a customer's information on braintree.
# Update done per field.
# ToDo: Make advance usage to make multiple updates

def braintree_update_customer(id, field_name, field_value,*args, **kwargs):
    try:
        result = braintree.Customer.update(str(id), {
            field_name: field_value
        })
        return True
    except:
        return False



def braintree_vault_user_payment_info(args):
    customer = braintree_create_customer(args)


def braintree_cancel_subscription(id):
    try:
        return braintree.Subscription.cancel(id)
    except braintree.NotFoundError:
        return None


def braintree_get_subscription(sub_id):
    if sub_id == None:
        return None
    try:
        return braintree.Subscription.find(sub_id)
    except braintree.NotFoundError:
        return None


# Subscribe's the user to the given plan id
# using the payment_token obtained from customer
# tokens. Returns the subscription result object
# or None if subscription could not happen.
def braintree_subscribe_user(payment_token, plan_id):
    result = braintree.Subscription.create({
        "payment_method_token": payment_token,
        "plan_id": plan_id
    })

    if result.is_success:
        return result.subscription
    else:
        print result.errors
        return None
