from django.conf.urls import patterns
from app.views import view

urlpatterns = patterns('',
    (r'^$', view),
)
