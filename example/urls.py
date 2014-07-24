from django.conf.urls import patterns
from .views import view

urlpatterns = patterns('',
    (r'^$', view),
)
