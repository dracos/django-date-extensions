from django.db.models import Model

from approximate_date.django.fields import VagueDateField


class TestModel(Model):
    start = VagueDateField()
    can_be_null = VagueDateField(null=True)

    def __unicode__(self):
        return u'%s' % str(self.start)
