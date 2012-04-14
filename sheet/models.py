from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Sheet(models.Model):
    """
    It's used to keep track of related qands.
    """
    user = models.ManyToManyField(User)
    title = models.TextField('Title')
    des = models.TextField('Description', blank=True)

    def __unicode__(self):
        return u'%s_%s' % (self.user, self.title)
