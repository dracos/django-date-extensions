from os import path

DEBUG = True

SECRET_KEY = 'x9i*)8dp_i=r1o(p%0-g*^sz@_(631+_tjr=e-t04vj2!@l$8a'
ROOT_URLCONF = 'example.urls'
INSTALLED_APPS = (
    'django_date_extensions',
)


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [path.abspath(path.join(path.dirname(__file__), 'templates'))],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ]
        },
    }
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'example.sqlite3',
    }
}
