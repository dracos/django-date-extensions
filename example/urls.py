from django.conf.urls import url
from .views import view

urlpatterns = [
    url(r'^$', view),
]
