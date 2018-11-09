DEBUG = True

SECRET_KEY = "x9i*)8dp_i=r1o(p%0-g*^sz@_(631+_tjr=e-t04vj2!@l$8a"
ROOT_URLCONF = "examples.django.form_fields.urls"
INSTALLED_APPS = ("approximate_date.django", "examples.django.form_fields")


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
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
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": "examples.sqlite3"}
}
