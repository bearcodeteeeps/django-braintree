# django-braintree
A subscription management system for braintree in django

This is a simple subscription manage system for django using the braintree API.

Still under development.

You are welcome to contribute.

# Using the app

1. To use this project, clone the repository.
2. Copy the payment app into your django project.
3. Add payment to your installed apps
4. In your main settings.py file define the following:

  - change this to production on your live site
    ```
    BRAINTREE_ENVIRONMENT = braintree.Environment.Sandbox
    ```  
  - Get this info from braintree console online
    ```
    BRAINTREE_MERCHANT_ID = "Your merchant id"
    BRAINTREE_PUBLIC_KEY = "Your public key"
    BRAINTREE_PRIVATE_KEY = "Your private key"
    ```
  - NOTE: Make sure the plan names are consistent i.e they are all lowercase.
  - A tuple of tuples of the form (plan_name, plan_description)
  - The list below is for explaining purposes
    ```
    BRAINTREE_PLANS = (
      ('monthly', 'User is a monthly user'),
      ('yearly', 'User is an yearly user'),
      ('database', 'User is a database user')
    )
    ```
  - A dict which uses each plan name as a key and the value stored against it is the braintree plan id. You can get the braintree plan id from your braintree console.
    ```
    BRAINTREE_PLAN_IDS = {
      'monthly': "monthly",
      'yearly' : "yearly",
      'database' : "database"
    }
    ```
  - If subscription is successful this redirect is used
  ```
  BRAINTREE_SUCCESS_URL = 'SUCCESS' # should be a valid url in the app
  ```
  - If subscription failed this redirect is used
  ```
  BRAINTREE_FAIL_URL = 'FAIL' # should be a valid url in the app
  ```
  - plan names which are exclusive i.e that user can only be a part of one exclusive plan. If user wants to become part of another exclusive plans, his previous plans will be gone.
  ```
  BRAINTREE_EXCLUSIVE_GROUPS = ['monthly', 'yearly']
  ```
5. Next, add the following to your root url file
  ```
  url(r'^payment/', include(payment.urls, namespace = 'payment'))
  ```
6. Run python manage.py test payment to verify the app is working.


If you have issues, raise them in the issues tab. 

Hope this helps the community!
