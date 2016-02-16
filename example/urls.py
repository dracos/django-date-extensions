from django.conf.urls.defaults import *
from .app.views import view

urlpatterns = patterns('',
    (r'^$', view),
)
