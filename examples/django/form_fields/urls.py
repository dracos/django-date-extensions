from django.urls import re_path

from examples.django.form_fields.views import view

urlpatterns = (
    re_path(r'^.*$', view),
)
