
# Set DEBUG to true so that we don't need to provide a 500.html template
# (django's debug on will be used instead).
DEBUG = True

SECRET_KEY = 'x9i*)8dp_i=r1o(p%0-g*^sz@_(631+_tjr=e-t04vj2!@l$8a'
ROOT_URLCONF = 'example.urls'
INSTALLED_APPS = (
    'django_date_extensions',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '',
    }
}
