import os

# Set DEBUG to true so that we don't need to provide a 500.html template
# (django's debug on will be used instead).
DEBUG = True
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print("base_dir=%s" % BASE_DIR)
print("templates=%s" % os.path.join(BASE_DIR, 'example/templates'))

SECRET_KEY = 'x9i*)8dp_i=r1o(p%0-g*^sz@_(631+_tjr=e-t04vj2!@l$8a'
ROOT_URLCONF = 'example.urls'
INSTALLED_APPS = (
    'django_date_extensions',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'example.sqlite3',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'example/templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            # ... some options here ...
        },
    },
]
