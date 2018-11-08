SECRET_KEY = 'abc'

INSTALLED_APPS = (
    'approximate_date.tests.django',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testing.sqlite3',
    }
}
