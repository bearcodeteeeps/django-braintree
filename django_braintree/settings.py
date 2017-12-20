"""
Django settings for scriptonomics project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import braintree
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n3j=$968eu%93x5&a0-@d+58+#$^$czi&=z&&u(40=z!wse61l'


# SECURITY WARNING: don't run with debug turned on in production!


# Set True when running on production to load the production settings.
ON_PRODUCTION = False

BRAINTREE_ENVIRONMENT = braintree.Environment.Sandbox
BRAINTREE_MERCHANT_ID = "bsg7wp979ryt28qy"
BRAINTREE_PUBLIC_KEY = "twyp2gbk5hj46qcw"
BRAINTREE_PRIVATE_KEY = "7e8202c3d56f48f35430bb40aa56764b"

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, "db.sqlite3")
    }
}


# Application definition

INSTALLED_APPS = (
    #'password_reset', #added 5.17.15 for password reset
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'payment'

)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware'
    # 'django_mobile.middleware.MobileDetectionMiddleware',
    # 'django_mobile.middleware.SetFlavourMiddleware',
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
)

SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
	#'TEMPLATE_LOADERS':'django_mobile.loader.Loader',
        #'TEMPLATE_CONTEXT_PROCESSORS':'django_mobile.context_processors.flavour',
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'scriptonomics.context_processors.mobile', #JUST ADDED
            ],
        },
    },
]

ROOT_URLCONF = 'django_braintree.urls'


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


BRAINTREE_PLANS = (
    ('monthly', 'User is a monthly user'),
    ('yearly', 'User is an yearly user'),
    ('database', 'User is a database user')
)
BRAINTREE_PLAN_IDS = {
    'monthly': "monthly",
    'yearly' : "yearly",
    'database' : "database"
}

BRAINTREE_SUCCESS_URL = 'SUCCESS'
BRAINTREE_FAIL_URL = 'FAIL'
BRAINTREE_EXCLUSIVE_GROUPS = ['monthly', 'yearly']